import datetime
import os
import logging

from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator
from airflow.contrib.operators import gcs_to_gcs

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

bash_cmd='gcloud beta compute --project MyProjectName ssh myMachineHostname --internal-ip --zone us-central1-a --command "ls /tmp/"'
with models.DAG(
        'bash_remote_gcp_machine_example',
        # Continue to run DAG once per day
        schedule_interval="@once",
        default_args=default_dag_args) as dag:

     start = DummyOperator(task_id='start')
    
     end = DummyOperator(task_id='end')
         
     bash_remote_gcp_machine = BashOperator(task_id='bash_remote_gcp_machine_task',bash_command=bash_cmd)


	
start >> bash_remote_gcp_machine >> end
 
   
