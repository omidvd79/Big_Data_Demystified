from airflow.utils.trigger_rule import TriggerRule
import datetime
import os
import logging

from airflow import DAG
from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
#from airflow.operators import dummy_operator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator

# Import operator from plugins
from airflow.contrib.operators import gcs_to_gcs
from airflow.utils import trigger_rule

  
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

from google.cloud import storage
client = storage.Client()
i=0 
with models.DAG('loop_over_gcs_bucket_files_example', schedule_interval=None, default_args=default_dag_args) as dag:

	start = DummyOperator(task_id='start')
	wait  = DummyOperator(task_id='wait',trigger_rule=TriggerRule.ONE_SUCCESS)	
	for blob in client.list_blobs('myBucket', prefix='myFolder/mySubfolder'):
		#task id must only contain alphanumeric chars
		bash_cmd="echo "+ str(blob.name)
		i=i+1
		bash_operator = BashOperator(task_id='bash_operator'+str(i),bash_command=bash_cmd)
		start.set_downstream(bash_operator)
		bash_operator.set_downstream(wait)

	end 	= DummyOperator(task_id='end')
wait >> end
