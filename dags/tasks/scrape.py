from jobspy import scrape_jobs
from util import get_job_id, current_datetime
from manage_mongo_db import save_to_mongodb
from pydantic_models import Job

# import pandas as pd

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', 50)


def scraper(**kwargs):
    try:
        ti = kwargs['ti']
        jobs = scrape_jobs(
            site_name=["linkedin", "glassdoor", "zip_recruiter", "indeed"],
            search_term="",
            location='USA',
            hyperlinks=True,
            is_remote=True,
            results_wanted=10,
        )
        ti.xcom_push(key="jobs_data", value=jobs)
        # return jobs
    except Exception as e:
        print(str(e))


def validate_data(**kwargs):
    validated_jobs = []
    ti = kwargs['ti']
    jobs_data = ti.xcom_pull(key="jobs_data", task_ids="call_scraper")
    # jobs = scraper()

    # Assume jobs is your dataframe
    if jobs_data:
        for _, item in jobs_data.iterrows():
            try:
                df_item = item.to_dict()
                jobId = get_job_id(df_item['job_url_hyper'], df_item['site'])

                job = Job(
                    jobId=jobId,
                    title=df_item['title'],
                    location=df_item['location'],
                    company=df_item['company'],
                    link=df_item['job_url_hyper'],
                    jobDescription=df_item['description'],
                    scapetime=current_datetime(),
                    jobPosted=df_item['date_posted']
                )
                print(jobId)
                validated_jobs.append(job.dict())
                # if not save_to_mongodb(job):
                #     pass
            except Exception as e:
                print(str(e))
                
    ti.xcom_push(key="validated_jobs_data", value=validated_jobs)