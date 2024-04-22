from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from tasks.scrape import scraper, validate_data
from tasks.manage_mongo_db import save_to_mongodb
from processor.grobid_parse import parsePDF
from processor.init_setup import download_and_initial_setup
from processor.data_validation import get_clean_csv
from processor.upload_to_snowflake import push_data_to_snowflake
with DAG(
    dag_id='job_scraping_workflow',
    default_args={'start_date': days_ago(1),
                  'execution_timeout': timedelta(minutes=30)},
    schedule_interval='0 23 * * *',
    catchup=False
) as dag:

    call_scraper = PythonOperator(
        task_id="call_scraper",
        python_callable=scraper,
        dag=dag
    )

    trigger_grobid = PythonOperator(
        task_id="validate_scraped_data",
        python_callable=validate_data,
        dag=dag
    )

    data_validation = PythonOperator(
        task_id="save_validate_data",
        python_callable=save_to_mongodb,
        dag=dag
    )

    call_scraper >> trigger_grobid >> data_validation >> upload_to_snowflake
