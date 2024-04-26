from database import connect_to_mongodb
from utils import extractKeywordFromLightSkillAPI, getAccessToken
from fastapi import HTTPException

def getJobMatchScore(skills, username, job_description):
    try:
        user_skills = []
        job_description_skills = []
        if skills:
            user_skills = skills
        else:
            db = connect_to_mongodb()
            collection = db["User"]
            user_document = collection.find_one({"username": username})
            if user_document:
                collection = db["user_skills"]
                user_skills = collection.find_one({"user_id": user_document["_id"]})["skills"]
            else:
                print("User not found.")
        token = getAccessToken()
        job_description_skills = extractKeywordFromLightSkillAPI(job_description, token)

        matched_skills = set(user_skills) & set(job_description_skills)
        missing_skills = set(job_description_skills) - set(user_skills)
        total_skills = len(job_description_skills)
        if total_skills > 0:
            match_percentage = round((len(matched_skills) / total_skills) * 100)
        else:
            match_percentage = 0

        return {
            "match_percentage": match_percentage,
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
