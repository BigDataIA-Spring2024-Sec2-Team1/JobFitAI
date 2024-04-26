from datetime import datetime
import re
import requests
import json


# Extracting jobId from job URLs
def get_job_id(job_url: str, site: str) -> str:
    try:
        if site == 'indeed':
            job_id = re.search(r'(?<=jk=)[\w-]+', job_url).group()
        elif site == 'zip_recruiter':
            job_id = re.search(r'(?<=lvk=)[\w-]+', job_url).group()
        elif site == 'linkedin':
            job_id = re.search(r'(?<=view/)\d+', job_url).group()
        elif site == 'glassdoor':
            job_id = re.search(r'(?<=jl=)\d+', job_url).group()
        else:
            job_id = None
        return job_id
    except Exception as e:
        print(job_url)
        print(site)
        print(str(e))


# Function to get the current datetime
def current_datetime():
    return datetime.now()


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


# def task2(**kwargs):
#     ti = kwargs['ti']
#     hook = MongoHook(mongo_conn_id="mongo_default")
#     client = hook.get_conn()
#     db = (
#         client.jobfit
#     )  # Replace "MyDB" if you want to load data to a different database
#     currency_collection = db.scraped_jobs
#     print(currency_collection)
#     print(f"Connected to MongoDB - {client.server_info()}")
#     result = {"jobId": "1009251000002",
#               "title": "Physician - Obesity Medicine",
#               "location": "United States",
#               "company": "Mochi",
#               "link": "<a href=\"https://www.glassdoor.com/job-listing/j?jl=1009251582608\">https://www.glassdoor.com/job-listing/j?jl=1009251582608</a>",
#               "jobDescription": "Mochi Health is an SF-based tele-health company for binge-eating disorder and obesity medicine. We provide wraparound services for obesity management, ranging from nutrition, fitness coaching, prescription medication, sleep therapy, and more. (www.joinmochi.com)\n\nWe are looking for experienced, independent providers who are passionate about obesity medicine and long-term patient relationships. We are a small startup that is rapidly scaling into many states across the country.\n\nRequirements:\n\n- 2+ years of work experience practicing obesity medicine and/or Endocrinology\n\n- Malpractice, with tail coverage, covered by Mochi\n\n- Flexible scheduling (24/7) choose-your-own hours\n\n- Custom-built EMR and protocols for longitudinal care model in obesity medicine\n\n- Ancillary services for high-quality patient care: lab testing, genetic testing and counseling, prior authorization and customer service support phone lines\n\n- Monthly academic lecture series on obesity management (optional)\n\nMDs licensed, active in 2+ states. Specialists in Obesity and Endocrinology Preferred. Hiring for all 50 States.\n\n**Please submit your resume as a PDF**\n\nJob Types: Part-time, Contract\n\nPay: $150.00 - $200.00 per hour\n\nBenefits:\n\n* Flexible schedule\n\nSchedule:\n\n* Choose your own hours\n\nApplication Question(s):\n\n* Please share any relevant experience you have working with patients in Obesity Management:\n* Please list all states that you are currently licensed in:\n* Have you previously been credentialed with any insurers?\n\nExperience:\n\n* GLP-1 prescribing: 1 year (Required)\n* Telemedicine (i.e. on camera using video chat): 1 year (Required)\n\nLicense/Certification:\n\n* Medical License (Required)\n\nWork Location: Remote",
#               "scapetime": "2024-04-24T20:50:21.676Z",
#               "jobPosted":  "2024-04-24T00:00:00.000Z"
#               }
#     # d = json.loads(result)
#     currency_collection.insert_one(result)
