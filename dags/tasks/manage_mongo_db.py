# # from pymongo import MongoClient
# # from tasks.pydantic_models import Job
# # from . import collection
# from airflow.providers.mongo.hooks.mongo import MongoHook
# # from typing import List, Dict
# from dotenv import load_dotenv
# import os

# load_dotenv()


# MONGO_SERVER = os.getenv("MONGO_SERVER")
# MONGO_PORT = os.getenv("MONGO_PORT")
# MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
# hook = MongoHook(mongo_conn_id="mongo_default")
# client = hook.get_conn()
# db = (
#     client.jobfit
# )  # Replace "MyDB" if you want to load data to a different database
# # client = MongoClient(f'mongodb://{MONGO_SERVER}:{MONGO_PORT}/')
# # db = client[MONGO_DB_NAME]
# # jobs_collection = db['jobs']


# def task3(**kwargs):
#     ti = kwargs['ti']
#     job_posting_list = ti.xcom_pull(
#         key="jobs_data", task_ids="validate_scraped_data")
#     if job_posting_list:
#         print(len(job_posting_list))


# # def save_to_mongodb(**kwargs):
# #     ti = kwargs['ti']
# #     job_posting_list = ti.xcom_pull(
# #         key="jobs_data", task_ids="validate_scraped_data")
# #     scraped_jobs_collection = db.job_data
# #     print(scraped_jobs_collection)
# #     print(job_posting_list)
# #     # print(f"Connected to MongoDB - {client.server_info()}")
# #     if job_posting_list and len(job_posting_list):
# #         print("job_posting_list ==> inside save_to_mongodb")
# #         for job in job_posting_list:
# #             # result = {"jobId": "1009251000002",
# #             #         "title": "Physician - Obesity Medicine",
# #             #         "location": "United States",
# #             #         "company": "Mochi",
# #             #         "link": "<a href=\"https://www.glassdoor.com/job-listing/j?jl=1009251582608\">https://www.glassdoor.com/job-listing/j?jl=1009251582608</a>",
# #             #         "jobDescription": "Mochi Health is an SF-based tele-health company for binge-eating disorder and obesity medicine. We provide wraparound services for obesity management, ranging from nutrition, fitness coaching, prescription medication, sleep therapy, and more. (www.joinmochi.com)\n\nWe are looking for experienced, independent providers who are passionate about obesity medicine and long-term patient relationships. We are a small startup that is rapidly scaling into many states across the country.\n\nRequirements:\n\n- 2+ years of work experience practicing obesity medicine and/or Endocrinology\n\n- Malpractice, with tail coverage, covered by Mochi\n\n- Flexible scheduling (24/7) choose-your-own hours\n\n- Custom-built EMR and protocols for longitudinal care model in obesity medicine\n\n- Ancillary services for high-quality patient care: lab testing, genetic testing and counseling, prior authorization and customer service support phone lines\n\n- Monthly academic lecture series on obesity management (optional)\n\nMDs licensed, active in 2+ states. Specialists in Obesity and Endocrinology Preferred. Hiring for all 50 States.\n\n**Please submit your resume as a PDF**\n\nJob Types: Part-time, Contract\n\nPay: $150.00 - $200.00 per hour\n\nBenefits:\n\n* Flexible schedule\n\nSchedule:\n\n* Choose your own hours\n\nApplication Question(s):\n\n* Please share any relevant experience you have working with patients in Obesity Management:\n* Please list all states that you are currently licensed in:\n* Have you previously been credentialed with any insurers?\n\nExperience:\n\n* GLP-1 prescribing: 1 year (Required)\n* Telemedicine (i.e. on camera using video chat): 1 year (Required)\n\nLicense/Certification:\n\n* Medical License (Required)\n\nWork Location: Remote",
# #             #         "scapetime": "2024-04-24T20:50:21.676Z",
# #             #         "jobPosted":  "2024-04-24T00:00:00.000Z"
# #             #         }
# #             if scraped_jobs_collection.find_one({"jobId": job["job_id"]}) is not None:
# #                 scraped_jobs_collection.insert_one(job)

# # def check_duplicate(job_id):
# #     return jobs_collection.find_one({"jobId": job_id}) is not None


# # def save_to_mongodb(**kwargs):
# #     validated_jobs_data: List[Dict]
# #     ti = kwargs['ti']
# #     validated_jobs_data = ti.xcom_pull(
# #         key="validated_jobs_data", task_ids="validate_scraped_data")
# #     if len(validated_jobs_data):
# #         for jobs_data in validated_jobs_data:
# #             try:
# #                 if not check_duplicate(jobs_data['jobId']):
# #                     jobs_collection.insert_one(jobs_data)
# #                     print(f"inserted=>{jobs_data['jobId']}")
# #             except Exception as e:
# #                 print(str(e))
