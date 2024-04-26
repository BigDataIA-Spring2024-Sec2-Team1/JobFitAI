from database import connect_to_mongodb
from utils import extractKeywordFromLightSkillAPI, getAccessToken, get_gpt_response
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


def getExperienceBulletPoints(resume_text,skills, username, job_description):
    try:
        output = []
        system_role = "you have tasked to extract experience section from the resume"
        bullet_point_system_role = "As a system, generate a bullet point for the experience section utilizing the provided project experience and individual skills, all aligned with the given job description"
        prompt = f"""You have been provided with a resume containing various sections including personal information, education, skills, and experience.
        Your task is to extract the experience section from the resume
        Input Data:
            - Resume: \n{resume_text}\n"""
        output_prompt = """
        you have to Strictly adhere to the format provided in the example below when giving your extracted result.
        Example:
        {"experience" : [{"name": "abc pvt. ltd.", "experience": "worked on front end"}]} it should always be in a JSON format
        You should not add any explanation or any other text in the response
        """

        prompt_for_bullet_points = f"""
            You've been given the experience of a project and the skills of a person along with a job description. 
            Your task is to craft a new bullet point for the experience section, incorporating specific skills provided. 
            your newely created should not be present in the experience section provided and it should include the skills provided below
            """

        extractspecificExperience = prompt
        extractspecificExperience += output_prompt
        response = get_gpt_response(extractspecificExperience, system_role)
        exp = eval(response)
        if exp.get("experience"):
            for experience in exp.get("experience"):
                specific_experience = experience.get("name") + experience.get("experience")
                prompt_for_bullet_points += f"""
                    Input Data:
                            - Experience: {experience},
                            - skills: {skills},
                            - job_description: {job_description}
                    """    
                prompt_for_bullet_points += """
                    You should follow below format for creating new experience bullet point
                        1) Use action verbs in the past tense to show your previous experience.
                        2) Include keywords and skills directly from the job posting in your achievements.
                        3) should follow simple formula: success verb + noun + metric + outcome
                        Review examples of achievements:
                        - Organized a sold out charity event for 300 people and raised $500,000.
                        - Conducted compliance training for 100+ managers virtually across five locations that reduced company costs by 50%.
                        - Implemented new payroll and tax accounting systems that saved firm $2 million over 5 years.

                    you have to Strictly adhere to the format provided in the example below when giving your result.
                    Example:
                    {"bullet_point" : "worked on frontend"} it should always be in a JSON format
                    You should not add any explanation or any other text in the response
                """
                res = get_gpt_response(prompt_for_bullet_points, bullet_point_system_role)
                res = eval(res)
                output.append({"name": experience.get("name"), "experience": experience.get("experience"), "bullet_point": res.get("bullet_point")})
        else:
            pass
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
