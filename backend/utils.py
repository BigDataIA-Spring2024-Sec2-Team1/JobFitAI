from pinecone_util import EMBEDDING_MODEL
from database import connect_to_mongodb
from dotenv import load_dotenv
import boto3
from fastapi import UploadFile, HTTPException
from botocore.exceptions import NoCredentialsError, ClientError
from pydparser import ResumeParser
from pydparser import utils
from constants import RESUME_SECTIONS_GRAD, EMBEDDING_MODEL, JOB_FIT_INDEX_NAME
from tempfile import NamedTemporaryFile
import requests
import json
import re
import openai
from pinecone_util import Pinecone
import os
import warnings
warnings.filterwarnings(
    action="ignore", message="unclosed", category=ResourceWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()


OPENAI_API_KEY = "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"
PINECONE_API_KEY = "432efbce-a192-4eb1-bba7-6b46fb18f1b5"

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def upload_to_s3(file: UploadFile, s3_filename: str):
    try:
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, s3_filename)
        return {"message": f"Successfully uploaded {s3_filename} to {S3_BUCKET_NAME}."}
    except NoCredentialsError:
        raise HTTPException(
            status_code=500, detail="AWS credentials not found")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Client error with S3: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def read_from_s3(s3_filename: str):
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_filename)
        file_content = response['Body'].read()
        return file_content
    except NoCredentialsError:
        raise HTTPException(
            status_code=500, detail="AWS credentials not found")
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Client error with S3: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def parseResume(file: UploadFile, text=True, extract_skills=True):
    try:
        try:
            token = getAccessToken()
            skills = []
            _temp_file = NamedTemporaryFile(delete=False)
            contents = file.file.read()
            with _temp_file as f:
                f.write(contents)
            text_data = utils.extract_text(
                _temp_file.name, f".{file.filename.split('.')[-1]}")
            if extract_skills:
                skills = extractKeywordFromLightSkillAPI(text_data, token)
            if text:
                data = text_data
            else:
                data = extract_entity_sections_grad(text_data)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500, detail='Error on uploading the file')
        finally:
            file.file.close()
            os.remove(_temp_file.name)
        return {"message": f"Successfully parse the file", "text": data, "skills": skills}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")


def extract_entity_sections_grad(text):
    try:
        text_split = [i.strip() for i in text.split('\n')]
        # sections_in_resume = [i for i in text_split if i.lower() in sections]
        entities = {}
        key = False
        for phrase in text_split:
            if len(phrase) == 1:
                p_key = phrase
            else:
                p_key = set(phrase.lower().split()) & set(RESUME_SECTIONS_GRAD)
            try:
                p_key = list(p_key)[0]
            except IndexError:
                pass
            if p_key in RESUME_SECTIONS_GRAD:
                if p_key not in entities:
                    entities[p_key] = []
                key = p_key
            elif key and phrase.strip():
                entities[key].append(phrase)
        return entities
    except Exception as e:
        print("error in extract_entity_sections_grad", e)
        return {"message": f"Unexpected error occured, {e}"}


def cleanExperienceSection(text, date=False, output_format="array"):
    try:
        pattern = r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Sep(?:tember)|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d+\b(?:\s*(?:–|-|–|–)\s*\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d+)?'
        if date:
            text_with_dates = []
            for i in text:
                _text = i.replace('•', '').strip()
                if (_text.strip() == ""):
                    continue
                _text = utils.remove_non_readable_chars(_text)
                text_with_dates.append(_text)
            if output_format == "array":
                return text_with_dates
            elif output_format == "str":
                return " ".join(text_with_dates)
            else:
                return text_with_dates
        else:
            text_without_dates = []
            for i in text:
                _text = re.sub(pattern, '', i).replace('•', '')
                if (_text.strip() == ""):
                    continue
                _text = utils.remove_non_readable_chars(_text)
                text_without_dates.append(_text.strip())
            if output_format == "array":
                return text_without_dates
            elif output_format == "str":
                return " ".join(text_without_dates)
            else:
                return text_without_dates
    except Exception as e:
        print("Error occured during cleaning experience section")


def extractKeywordFromLightSkillAPI(text, token):
    try:
        headers = {
            'Authorization': f'Bearer {eval(token).get("access_token")}', 'Content-Type': "application/json"}

        url = "https://emsiservices.com/skills/versions/latest/extract"

        payload = {
            "text": text,
            "confidenceThreshold": 0.5
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        res = json.loads(response.text)

        if "message" in res and res["message"] == "Token expired":
            raise Exception("TOKEN_EXPIRED")

        skills = []
        for i in res['data']:
            skills.append(i["skill"]["name"])
        return skills
    except Exception as e:
        print("error -> ", e.args)
        print("error more details -> ", e)
        if e.args[0] == "TOKEN_EXPIRED":
            token = json.loads(getAccessToken())
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")


def getAccessToken():
    url = "https://auth.emsicloud.com/connect/token"
    payload = "client_id=4v22ofaxe2m1np9c&client_secret=JAjNxQy0&grant_type=client_credentials&scope=emsi_open"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text


def skillsSimilarity(skills, namespace, resume_text):
    try:
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "None"))
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(JOB_FIT_INDEX_NAME)
        skills_embedding = client.embeddings.create(
            input=skills, model=EMBEDDING_MODEL).data[0].embedding
        match_res = index.query(
            top_k=2, vector=skills_embedding, namespace=namespace, include_metadata=True)
        jd_match_res = index.query(
            top_k=3, vector=skills_embedding, namespace="skills", include_metadata=True)
        designations = []
        _similar_skills = []
        jd_skills = []
        for i in match_res["matches"]:
            meta = i["metadata"]["metadata"]
            meta = eval(meta)
            _similar_skills.append(meta.get("skills"))
            if meta.get("designation") and type(meta.get("designation")) != type([]):
                designations.append(meta.get("designation"))
            if type(meta.get("designation")) == type([]):
                for j in meta.get("designation"):
                    if j and len(j) < 50:
                        designations.append(j)
        for i in jd_match_res["matches"]:
            jd_meta = i["metadata"]["extras"]
            jd_meta = eval(jd_meta)
            jd_skills.append(jd_meta.get("skills"))
        newDesig = user_categorization_gpt(skills, resume_text, designations)
        return {"similar_profile_skills": _similar_skills, "designations": [newDesig.split(":")[-1]], "jd_skills": jd_skills}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")


def get_gpt_response(q_prompt, system_role):
    try:
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "None"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": q_prompt},
            ],
            max_tokens=10000,
            stream=True,
        )
        text = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                text = text + chunk.choices[0].delta.content
        return text
    except openai.error.OpenAIError as e:
        print(f"An OpenAI API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred at gpt response: {e}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")
    return None


def user_categorization_gpt(skills, resume_text, designation):
    try:
        system_role = "You are a Hiring Manager tasked with analyzing a candidate's resume and skills to suggest the most appropriate job title. Your role involves a detailed evaluation of the experience and project section of the resume to determine a fitting designation, based on the provided information."
        prompt = f"""
            As a Hiring Manager, your task is to evaluate the candidate's resume and skills to suggest an appropriate job title.
            Based on the provided resume details, skill set and possible designations, determine the most fitting designation for the candidate.

            - Resume Details: \n{resume_text}\n
            - Skills: \n{skills}\n
            - Possible Designations: \n{designation}\n

            Focus on the experience and project section of the resume to assess the candidate's qualifications and suggest a suitable job title.
            Please Strictly adhere to the format provided in the example below when giving your recommendation.

            Example:
            Title: Software Engineer

            You should not add any explanation or any other text except the designation in the response
            """
        response = get_gpt_response(prompt, system_role)
        return response
    except Exception as e:
        print("error in user_cat_gpt", e)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")


def suggestKeywords(similar_skills, resume_text, designation, num_of_skills):
    try:
        system_role = "You are a Senior Hiring Manager tasked with analyzing a candidate's resume and skills to suggest the most appropriate keywords and skills. Your role involves a detailed evaluation of the experience and project section of the resume to determine a fitting skills, based on the provided information."
        prompt = f"""
            As a Hiring Manager, your task is to evaluate the candidate's resume and skills to suggest an appropriate skills required for the job.
            Based on the provided resume details, skills which are mostly seen in similar profile and designations,
            your task is to Suggest the NEW list of keywords to improve the resume for the candidate.
            Ensure that the newly suggested keywords are not already mentioned in the candidate's resume details but are relevant and derived from similar skills.
            - Resume Details: \n{resume_text}\n
            - Skills: \n{similar_skills}\n
            - Designations: \n{designation}\n
            """

        prompt_res_fmt = """
            Please Strictly adhere to the format provided in the example below when giving your recommendation.

            Example:
            {"Skills" : ['Java', 'Python', 'AWS']} it should always be in a JSON format
            You should not add any explanation or any other text in the response
        """

        prompt += prompt_res_fmt

        prompt_for_top_k = f"""
            As a Hiring Manager, your objective is to identify and rank the top {num_of_skills} skills necessary for a specific job title.
            This task involves analyzing a list of skills and matching them to job titles to determine the most relevant and critical skills for each role.
            Please follow the instructions below to complete this task:

            Instructions:
            1. Review the list of skills provided.
            2. Examine the job designation(s) specified.
            3. Based on your analysis, select and rank the top 10 skills that are most pertinent and valuable for the given job designation.
            4. Ensure that your selection is tailored to the requirements and expectations of the job role.

            Input Data:
            - List of Skills: {similar_skills}
            - Job Designation: {designation}

            Your task is to output a ranked list of the top 10 skills for the specified job designation, considering the relevance and importance of each skill to the role
        """

        prompt_for_top_k += prompt_res_fmt

        response = get_gpt_response(prompt, system_role)

        response_top_k = get_gpt_response(prompt_for_top_k, system_role)
        return {"response": response, "top_k": response_top_k}
    except Exception as e:
        print("error in suggestKeyword", e)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")


def addSkillToUserDB(skills, username):
    try:
        db = connect_to_mongodb()
        collection = db["User"]
        user_document = collection.find_one({"username": username})
        if user_document:
            user_skills = {
                "user_id": user_document["_id"],
                "skills": skills,
                "username": username
            }
            collection = db["user_skills"]
            result = collection.insert_one(user_skills)
        else:
            print("User not found.")
    except Exception as e:
        print("error in addskilltouserdb", e)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")



def getJobSuggesions(username=""):
    try:
        job_descriptions = []
        if username:
            db = connect_to_mongodb()
            collection = db["User"]
            user_document = collection.find_one({"username": username})
            if user_document:
                collection = db["user_skills"]
                user_skills = collection.find_one(
                    {"user_id": user_document["_id"]})["skills"]

                if user_skills:
                    job_fit_index_name = 'job-fit'
                    index = pc.Index(job_fit_index_name)
                    EMBEDDING_MODEL = "text-embedding-3-small"
                    query = str(user_skills)

                    xqq = openai_client.embeddings.create(
                        input=query, model=EMBEDDING_MODEL).data[0].embedding

                    match_res = index.query(top_k=100, vector=xqq,
                                            namespace="description", include_metadata=True)
                    result_list = match_res["matches"]
                    jobids = [res["id"] for res in result_list]
                    print(jobids)

                    jobs_collection = db["scraped_jobs"]
                    query = {"job_id": {"$in": jobids}}
                    results = jobs_collection.find({})
                    if results:
                        print(results[0])
                        for doc in results:
                            job_desc = {"title": doc["title"],
                                        "company": doc["company"],
                                        "location": doc["location"],
                                        "description": doc["description"],
                                        "listed_at": doc["listed_at"],
                                        "job_id": doc["job_id"],
                                        "apply_url":doc["apply_url"],
                                        "job_posted": doc["job_posted"]}
                            job_descriptions.append(job_desc)
                    else:
                        print("Scraped jobs not found")
            else:
                print("User not found.")
        else:
            print("Username is not valid.")
        return job_descriptions
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}")
