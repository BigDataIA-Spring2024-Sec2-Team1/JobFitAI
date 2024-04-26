# from datetime import datetime
import time
import datetime
import pytz
from typing import List
from airflow.providers.mongo.hooks.mongo import MongoHook
from tasks.linkedIn import Linkedin
from tasks.pydantic_models import JobPosting
from tasks.datetime_manage import current_datetime

api = Linkedin('sudarshandudhe.masters@gmail.com', 'SD@12010220')
hook = MongoHook(mongo_conn_id="mongo_default")
client = hook.get_conn()
db = (
    client.jobfit
)  # Replace "MyDB" if you want to load data to a different database


def current_datetime():
    return datetime.datetime.now(pytz.timezone('America/New_York'))


def getprofile():
    profile = api.get_profile('sudarshandudhe')
    print(profile)


def get_jobs_details(**kwargs):
    try:
        print("get_jobs_details")
        print("get_jobs_details")
        ti = kwargs['ti']
        search_keywords = ""
        _limit = 100
        location = "USA"
        jobs = api.search_jobs(keywords=search_keywords,
                               limit=_limit,
                               location_name=location)

        job_posting_data_list = []
        for job in jobs:
            job_id = extract_job_id(job)
            if job_id:
                job_data = api.get_job(job_id)
                job_posting_data_list.append(job_data)
        # return job_posting_data_list
        ti.xcom_push(key="jobs_data", value=job_posting_data_list)
    except Exception as e:
        print(str(e))


def extract_job_id(job_data: dict) -> int:
    entity_urn = job_data.get('entityUrn')
    if entity_urn:
        parts = entity_urn.split(':')
        if len(parts) > 2:
            return int(parts[-1])
    return None


def parse_job_posting(**kwargs):
    # try:
    # job_posting_data_list: List[dict]
    ti = kwargs['ti']
    job_posting_data_list = ti.xcom_pull(
        key="jobs_data", task_ids="call_scraper")
    job_posting_list = []
    scrape_time = current_datetime().strftime('%Y-%m-%d %H:%M:%S')
    if len(job_posting_data_list):
        for data in job_posting_data_list:
            try:
                job_data = {
                    "title": data.get("title"),
                    "company": data.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany", {}).get("companyResolutionResult", {}).get("name") or data.get("companyDetails", {}).get("com.linkedin.voyager.jobs.JobPostingCompanyName", {}).get("companyName") or "",
                    "location": data.get("formattedLocation"),
                    "description": data.get("description", {}).get("text"),
                    "apply_url": data.get("applyMethod", {}).get("com.linkedin.voyager.jobs.OffsiteApply", {}).get("companyApplyUrl") or data.get("applyMethod", {}).get("com.linkedin.voyager.jobs.ComplexOnsiteApply", {}).get("easyApplyUrl") or "",
                    "listed_at": data.get("listedAt"),
                    "job_id": data.get("jobPostingId"),
                    "job_posted": scrape_time,
                }
                job_posting = JobPosting.parse_obj(job_data)
                # job_posting = parse_job_posting(job_data)
                if job_posting:
                    job_posting_list.append(job_posting.dict())
                    # scraped_jobs_collection.insert_one(job_posting.dict())
                    time.sleep(0.1)
            except Exception as e:
                print(data)
                print(str(e))
        print(job_posting_list[0])
        # save_to_mongodb(job_posting_list)
        scraped_jobs_collection = db.scraped_jobs
        print(scraped_jobs_collection)
        print(len(job_posting_list))
        # print(f"Connected to MongoDB - {client.server_info()}")
        if len(job_posting_list):
            print("job_posting_list ==> inside save_to_mongodb")
            for job in job_posting_list:
                if scraped_jobs_collection.find_one({"job_id": job["job_id"]}) is None:
                    scraped_jobs_collection.insert_one(job)
                    time.sleep(0.1)
                # time
                # pass
        ti.xcom_push(key="job_posting_list", value=job_posting_list)
    else:
        ti.xcom_push(key="jobs_data", value=[])
    # return job_posting_list
    # ti.xcom_push(key="job_posting_list", value=job_posting_list)
    # ti.xcom_push(key="validated_jobs_data", value=[])
    # except Exception as e:
    #     print(str(e))
    #     print(data)
    #     return None


def save_to_mongodb(job_posting_list):
    # ti = kwargs['ti']
    # job_posting_list = ti.xcom_pull(
    #     key="jobs_data", task_ids="validate_scraped_data")
    scraped_jobs_collection = db.job_data
    print(scraped_jobs_collection)
    print(len(job_posting_list))
    # print(f"Connected to MongoDB - {client.server_info()}")
    if len(job_posting_list):
        print("job_posting_list ==> inside save_to_mongodb")
        for job in job_posting_list:
            if not scraped_jobs_collection.find_one({"jobId": job["job_id"]}) is not None:
                scraped_jobs_collection.insert_one(job)
