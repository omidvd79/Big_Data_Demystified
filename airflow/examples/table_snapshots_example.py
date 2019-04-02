import datetime
import os
import logging

from airflow import DAG
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator

from airflow.operators.dummy_operator import DummyOperator

today_date = datetime.datetime.now().strftime("%Y%m%d")

destination_cloud_storage_uris1 = 'gs://data_lake/table_snapshot/' +'dt=' + today_date+ '/file-*.avro'
  

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




with DAG(dag_id='table_snapshot', 
		# Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1), 
        default_args=default_dag_args) as dag:
    
    start = DummyOperator(task_id='start')
    
    end = DummyOperator(task_id='end')
    
    
    bq_table_snapshot = BigQueryToCloudStorageOperator(
		task_id='bq_table_snapshot',
		source_project_dataset_table='MyProjectID.DATA_LAKE.table_name',
		destination_cloud_storage_uris=[destination_cloud_storage_uris1],
		compression='Snappy',
		export_format='Avro',
		bigquery_conn_id='bigquery_default' 
    )
    

start >> bq_table_snapshot >> end