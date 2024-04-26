from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.utils.dates import days_ago
from datetime import timedelta
# from tasks.scrape import scraper, validate_data
from tasks.manage_mongo_db import task3
from tasks.linkedIn_util import parse_job_posting, get_jobs_details


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


with DAG(
    dag_id='job_scraping_workflow',
    default_args={'start_date': days_ago(1),
                  'execution_timeout': timedelta(minutes=30)},
    # schedule_interval='0 23 * * *',
    catchup=False
) as dag:

    call_scraper = PythonOperator(
        task_id="call_scraper",
        python_callable=get_jobs_details,
        dag=dag
    )

    parse_jobs_data = PythonOperator(
        task_id="validate_scraped_data",
        python_callable=parse_job_posting,
        dag=dag
    )

    save_to_db = PythonOperator(
        task_id="save_validate_data",
        python_callable=task3,
        dag=dag
    )

    call_scraper >> parse_jobs_data >> save_to_db
