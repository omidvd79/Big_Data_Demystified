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



#this assume you have configured HMAC authentication via Boto3 to access AWS s3 via GSUTIL 


rsync_uninstalls_cmd=			      'gcloud beta compute --project 	myProject ssh apps-flyer	--internal-ip --zone us-central1-c --command "sudo -u omid gsutil -m rsync  -r -x \".*_SUCCESS.*$\"  s3://af-ext-reports/xxx/data-locker-hourly/t=uninstalls/  gs://data_lake_ingestion_us/apps_flyer/t=uninstalls/"'
rsync_installs_cmd=  			      'gcloud beta compute --project 	myProject ssh apps-flyer	--internal-ip --zone us-central1-c --command "sudo -u omid gsutil -m rsync  -r -x \".*_SUCCESS.*$\"  s3://af-ext-reports/xxx/data-locker-hourly/t=installs/  gs://data_lake_ingestion_us/apps_flyer/t=installs/"'
rsync_organic_uninstall_cmd=  	'gcloud beta compute --project 	myProject ssh apps-flyer	--internal-ip --zone us-central1-c --command "sudo -u omid gsutil -m rsync  -r -x \".*_SUCCESS.*$\"  s3://af-ext-reports/xxx/data-locker-hourly/t=organic_uninstalls/  gs://data_lake_ingestion_us/apps_flyer/t=organic_uninstalls/"'


with models.DAG(
        'apps_flyer_sync_data_locker',
        # Continue to run DAG once per day
        schedule_interval='@hourly',
        default_args=default_dag_args) as dag:

	#dummy - proceed only if success
	start = DummyOperator(task_id='start')
	end = DummyOperator(task_id='end')
	
	rsync_uninstalls 		= BashOperator( task_id='rsync_uninstalls',	bash_command=rsync_uninstalls_cmd,dag=dag)
	rsync_installs 			= BashOperator( task_id='rsync_installs',	bash_command=rsync_installs_cmd,dag=dag)
	rsync_organic_uninstall = BashOperator( task_id='organic_uninstall',bash_command=rsync_organic_uninstall_cmd,dag=dag)



start >> rsync_uninstalls 			>> end
start >> rsync_installs 			>> end
start >> rsync_organic_uninstall 	>> end
