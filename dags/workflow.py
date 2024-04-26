from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.utils.dates import days_ago
from datetime import timedelta
# from tasks.scrape import scraper, validate_data
# from tasks.manage_mongo_db import task3
from tasks.embeddings import create_embeddings
from tasks.linkedIn_util import parse_job_posting, get_jobs_details


def task1(**kwargs):
    pass


def task2(**kwargs):
    pass


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
        python_callable=create_embeddings,
        dag=dag
    )

    call_scraper >> parse_jobs_data >> save_to_db
