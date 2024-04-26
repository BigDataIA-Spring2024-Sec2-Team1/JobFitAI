from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
import requests
from utils import getJobSuggesions
from datetime import datetime
import warnings
from pydantic import BaseModel
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
# import nltk
# nltk.download('stopwords')
load_dotenv()

warnings.filterwarnings("ignore")

# SF_USERNAME = os.getenv("USERNAME")
# SF_PASSWORD = os.getenv("PASSWORD")
# SF_ACCOUNT_IDENTIFIER = os.getenv("ACCOUNT_IDENTIFIER")
# DATABASE_NAME = os.getenv("DATABASE_NAME")
# TABLE_NAME = os.getenv("TABLE_NAME")
# WAREHOUSE_NAME = os.getenv("WAREHOUSE_NAME")
# STAGE_NAME = os.getenv("STAGE_NAME")
# STAGE_PATH = os.getenv("STAGE_PATH")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# @app.post("/upload")
# async def upload_file(files: UploadFile = File(...)):
#     try:
#         print("Uploading file to s3", files.filename,files.file)
#         s3_client.upload_fileobj(files.file, S3_BUCKET_NAME, files.filename)
#         print("file uploaded successfully")
#         triggerAirFlowPipeline(f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{files.filename}')
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#     return {"message": "File(s) uploaded successfully"}


@app.get("/")
def hello():
    return {"message": "Backend is running"}


class UserSkillDB(BaseModel):
    skills: List[str]
    username: str


class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    description: str
    apply_url: str
    listed_at: int
    job_id: int
    job_posted: datetime

    @classmethod
    def parse_obj(cls, obj):
        # Validate and parse the dictionary into the Pydantic model
        return cls(**obj)


class UserSkillDB(BaseModel):
    skills: List[str]
    username: str


class UserName(BaseModel):
    username: str


@app.post("/getJobSuggesions")
def getSuggesions(request: UserName):
    username = request.username
    job_descriptions = getJobSuggesions(username)
    return {"data": {"job_descriptions": job_descriptions}}


def triggerAirFlowPipeline(s3_url):
    airflow_base_url = 'http://host.docker.internal:8024'
    airflow_url = f"{airflow_base_url}/api/v1/dags/cfa_workflow/dagRuns"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Authorization": "Basic YWlyZmxvdzphaXJmbG93",
    }
    # data = {"conf": {"s3_uploaded_file": s3_url}}
    data = {}
    response = requests.post(airflow_url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        response_json = response.json()
        return (
            "DAG triggered successfully",
            response_json["dag_run_id"],
        )
    else:
        return f"Failed to trigger DAG: {response.text}", None, None

# @app.get("/get_sf_data")
# async def get_sf_data():
#     try:
#         print("calling function to get data from snowflake ")
#         data = view_table_from_snowflake()
#         return {"data":data}
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
#     return {"message": "File(s) uploaded successfully"}

# def view_table_from_snowflake():
#     try:
#         with create_engine(
#             f"snowflake://{SF_USERNAME}:{SF_PASSWORD}@{SF_ACCOUNT_IDENTIFIER}/"
#         ).connect() as connection:
#             connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
#             result = connection.execute(f"""SHOW TABLES LIKE '{TABLE_NAME}'""")
#             existing_tables = [row[1] for row in result.fetchall()]
#             print(existing_tables)
#             if TABLE_NAME.upper() in existing_tables:
#                 result_cursor = connection.execute(
#                     f"""SELECT * FROM {TABLE_NAME}"""
#                 )
#                 result = result_cursor.fetchall()
#                 # df_columns = list(result[0])
#                 # df = pd.DataFrame(result[1:], columns=df_columns)
#                 print("Data fetched successfully.")
#                 return result
#             else:
#                 print("Table does not exist.")
#                 return None
#     except Exception as e:
#         print(f"Error while viewing data from Snowflake: {e}")
#         return False
