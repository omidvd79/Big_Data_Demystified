import datetime
import os
import logging
from datetime import timedelta, date

from airflow import DAG
from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator
from airflow.contrib.operators import gcs_to_gcs
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.utils import trigger_rule

from google.cloud import storage


#from airflow.utils import trigger_rule

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
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}



 



bucket_name2='MyBucket'
prefix=''
delimiter=''
storage_client = storage.Client()
blobs = storage_client.list_blobs(bucket_name2, prefix=prefix, delimiter=delimiter)

def get_alphanumeric_task_id(a_string):
		
	isalnum = a_string.isalnum()
	#print('Is String Alphanumeric :', isalnum)
	alphanumeric_filter = filter(str.isalnum, a_string)
	alphanumeric_string = "".join(alphanumeric_filter)
	#remove / from file path
	return alphanumeric_string.replace("/", "__") 


with models.DAG(
        'import_ingestion',
        # Continue to run DAG once per day
        schedule_interval='@once',
        default_args=default_dag_args) as dag:

	start = DummyOperator(task_id='start')
	
	wait = DummyOperator(task_id='wait',trigger_rule="all_done")
    
	end = DummyOperator(task_id='end',trigger_rule="all_done")
	
	
	
	for blob in blobs:
		#print(blob.name)
		print_file = BashOperator( task_id='print_file_'+get_alphanumeric_task_id(blob.name),bash_command='echo "hello "+blob.name',dag=dag)
		start.set_downstream(print_file)
		print_file.set_downstream(wait)

	
wait >> end
