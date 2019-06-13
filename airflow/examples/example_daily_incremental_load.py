import datetime
import os
import logging

from airflow import DAG
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator

today_date = datetime.datetime.now().strftime("%Y%m%d")

#table_name = 'omid.test_results' + '$' + today_date
table_name = 'DATA.table' 
 

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}



delete_query = """
delete   from `DATA.table` 
where date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY)
          AND  DATE_SUB(CURRENT_DATE(), INTERVAL 0 DAY) 
"""

evya_query = """
SELECT
*

FROM
source_table
"""



with DAG(dag_id='example_daily_incremental_load', 
		# Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    
    start = DummyOperator(task_id='start')
    
    end = DummyOperator(task_id='end')
    
    logging.error('trying to bq_query: ')
    logging.error('table name: '+table_name)
   # sql = """ SELECT * FROM `omid.test1` """
    sql = evya_query
    bq_query = BigQueryOperator(
		task_id='bq_query',
		bql=sql,
		destination_dataset_table=table_name,
		bigquery_conn_id='bigquery_default',
		use_legacy_sql=False,
		write_disposition='WRITE_APPEND',
		create_disposition='CREATE_NEVER',
		allow_large_results='true',
		dag=dag
    )
    sql = delete_query
    bq_delete_query = BigQueryOperator(
		task_id='bq_delete_query',
		bql=sql,
		bigquery_conn_id='bigquery_default',
		use_legacy_sql=False,
		dag=dag
    )

start >> bq_delete_query >> bq_query >> end