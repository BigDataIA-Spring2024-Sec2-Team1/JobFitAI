from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import nltk
nltk.download('stopwords')
from utils import upload_to_s3, parseResume, skillsSimilarity, suggestKeywords
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
def hello_world():
    return JSONResponse(status_code=200, content="Hello there, Application is Healthy")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_filename = file.filename
        response = upload_to_s3(file, s3_filename)
        return JSONResponse(status_code=200, content=response)
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"An unexpected error occurred: {str(e)}"})


@app.post("/parse-resume")
async def parse_resume(text: bool = True, extract_skills:bool = True, file: UploadFile = File(...)):
    try:
        response = parseResume(file, text, extract_skills)
        return JSONResponse(status_code=200, content=response)
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"An unexpected error occurred: {str(e)}"})

class UserCategorizationRequest(BaseModel):
    skills: List[str]
    namespace: str
    resume_text: str

@app.post("/user-categorization")
def user_categorization(request: UserCategorizationRequest):
    try:
        response = skillsSimilarity(request.skills, request.namespace, request.resume_text)
        return JSONResponse(status_code=200, content=response)
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"An unexpected error occurred: {str(e)}"})

class SuggestKeywordRequest(BaseModel):
    similar_skills: List[str]
    resume_text: str
    designation: str
    num_of_skills: int

@app.post("/suggest-keyword")
def keyword_suggestion(request: SuggestKeywordRequest):
    try:
        response = suggestKeywords(request.similar_skills, request.resume_text, request.designation, request.num_of_skills)
        return JSONResponse(status_code=200, content=response)
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"An unexpected error occurred: {str(e)}"})
