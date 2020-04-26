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
    'concurrency':12,
    'max_active_runs':2,
    'catchup':False,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

from datetime import timedelta, date
 
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
 
 
### start & end date = delta period.
## -3 days?
delta=-440
start_date = datetime.date.today() + datetime.timedelta(delta)
end_date = datetime.date.today()

 


bash_run_report_remotly_cmd='gcloud beta compute --project gap---all-sites-1245 ssh search-console	--internal-ip --zone us-central1-c --command "sudo -u omid python /home/omid/search_analytics_api_sample.py"'
 


### init variables
bucket_name2='data_lake_ingestion_us'

def get_alphanumeric_task_id(a_string):
		
	isalnum = a_string.isalnum()
	#print('Is String Alphanumeric :', isalnum)
	alphanumeric_filter = filter(str.isalnum, a_string)
	alphanumeric_string = "".join(alphanumeric_filter)
	#remove / from file path
	return alphanumeric_string.replace("/", "__").replace(".", "_")  


with models.DAG(
        'search_console_with_quata',
        # Continue to run DAG once per day
        schedule_interval=None,
        default_args=default_dag_args) as dag:

	#dummy - proceed only if success
	start = DummyOperator(task_id='start')
	wait = DummyOperator(task_id='wait')

	end = DummyOperator(task_id='end')
	
	for single_date in daterange(start_date, end_date):
		temp_date=single_date.strftime("%Y-%m-%d")
		day_after_single_date=single_date+ datetime.timedelta(days = 1)
		day_after_single_date=day_after_single_date.strftime("%Y-%m-%d")
		
		##notice trigger_rule="all_done"
		bash_run_report_remotly_cmd='gcloud beta compute --project 	gap---all-sites-1245 ssh search-console --internal-ip --zone us-central1-c --command "sudo -u omid python /home/omid/search_analytics_api_sample.py sc-domain:investing.com '+temp_date+" "+day_after_single_date+'"'
		run_report_remotly = BashOperator(task_id='run_report_remotly_'+temp_date,retries=2,retry_delay=datetime.timedelta(minutes=15),retry_exponential_backoff=True,max_retry_delay=datetime.timedelta(hours=48),bash_command=bash_run_report_remotly_cmd,trigger_rule="all_done")
		start.set_downstream(run_report_remotly)
		run_report_remotly.set_downstream(wait)

	mv_to_data_lake = BashOperator( task_id='mv_to_data_lake',bash_command='gcloud beta compute --project 	gap---all-sites-1245 ssh search-console --internal-ip --zone us-central1-c --command "sudo -u omid gsutil -m mv -r  /tmp/search* gs://data_lake_ingestion_us/search_console/"',dag=dag)
	
	load="""bq --location US load --source_format CSV --replace=true --skip_leading_rows 1 --allow_quoted_newlines DATA_LAKE_INGESTION_US.search_console_partition gs://data_lake_ingestion_us/search_console/*"""

	load_to_data_lake = BashOperator( task_id='load_to_data_lake',bash_command=load,dag=dag)
	
wait  >> mv_to_data_lake  >> load_to_data_lake >> end
