from pymongo import MongoClient
from pydantic_models import Job
from . import collection
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()


MONGO_SERVER = os.getenv("MONGO_SERVER")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(f'mongodb://{MONGO_SERVER}:{MONGO_PORT}/')
db = client[MONGO_DB_NAME]
jobs_collection = db['jobs']


def check_duplicate(job_id):
    return jobs_collection.find_one({"jobId": job_id}) is not None


def save_to_mongodb(**kwargs):
    validated_jobs_data: List[Dict]
    ti = kwargs['ti']
    validated_jobs_data = ti.xcom_pull(
        key="validated_jobs_data", task_ids="validate_scraped_data")
    for jobs_data in validated_jobs_data:
        try:
            if not check_duplicate(jobs_data['jobId']):
                jobs_collection.insert_one(jobs_data)
                print(f"inserted=>{jobs_data['jobId']}")
        except Exception as e:
            print(str(e))
