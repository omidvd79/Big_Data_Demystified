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

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

### start & end date = delta period.
## -7 days?
## deleta must be -3 or lower (negative number), -3 to produce days of history from today including today.
delta=-3
start_date = datetime.date.today() + datetime.timedelta(delta)
end_date = datetime.date.today()


bash_run_report_remotly_cmd='gcloud beta compute --project myProjectName ssh myInstanceNAme --internal-ip --zone us-central1-a --command "sudo -u omid python3 /home/omid/gam_data_transfer/report_example_using_service_account_with_date_range.py --start 2020-02-27 --end 2020-02-27"'

bash_gsutil_mv_cmd='gcloud beta compute --project ynet-data-myProjectName ssh myInstanceNAme --internal-ip --zone us-central1-a --command "sudo -u omid gsutil -m mv /tmp/*report_example_using_service_account_with_date_range* gs://myBucket/google/gam/example_report"'

#the python creates a random temporary file name suffix, so we delete the files in teh bucket before we proceed 
bash_cleanup_cmd='gsutil rm gs://myBucket/google/gam/example_report/*report_example_using_service_account_with_date_range_2020-02-26*'

with models.DAG(
        'run_example_gam_report_remote_machine',
        # Continue to run DAG once per day
        schedule_interval="@once",
        default_args=default_dag_args) as dag:

	start = DummyOperator(task_id='start')
	
	wait = DummyOperator(task_id='wait',trigger_rule="all_done")
    
	end = DummyOperator(task_id='end',trigger_rule="all_done")
	
	
	
	#notice if delta has to be negative, -3 or lower,  so will have some dates in date range - you wont have an operator.
	for single_date in daterange(start_date, end_date):
		temp_date=single_date.strftime("%Y-%m-%d")

		##notice trigger_rule="all_done"
		bash_cleanup_cmd='gsutil rm gs://myBucket/google/gam/example_report/*report_example_using_service_account_with_date_range_'+temp_date+'*'
		bash_cleanup = BashOperator(task_id='bash_cleanup_'+temp_date,retries=0,bash_command=bash_cleanup_cmd,trigger_rule="all_done")
		
		##notice trigger_rule="all_done"
		bash_run_report_remotly_cmd='gcloud beta compute --project ynet-data-analytics ssh scheduler2 --internal-ip --zone us-central1-a --command "sudo -u omid python3 /home/omid/gam_data_transfer/report_example_using_service_account_with_date_range.py --start '+temp_date+" --end "+temp_date+'"'
		run_report_remotly = BashOperator(task_id='run_report_remotly_'+temp_date,retries=0,bash_command=bash_run_report_remotly_cmd,trigger_rule="all_done")


		start.set_downstream(bash_cleanup)
		bash_cleanup.set_downstream(run_report_remotly)
		run_report_remotly.set_downstream(wait)

	##notice trigger_rule="all_done"
	run_gsutil_mv = BashOperator(task_id='bash_gsutil_mv_cmd',retries=0,bash_command=bash_gsutil_mv_cmd,trigger_rule="all_done")
	
	load_to_bq_from_gcs = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
    		task_id='load_to_bq_from_gcs',
    		source_objects='*',
    		skip_leading_rows=1,
    		create_disposition='CREATE_NEVER',
    		write_disposition='WRITE_TRUNCATE', #overwrite?
    		bucket='myBucket/google/gam/example_report',
    		destination_project_dataset_table='DATA_LAKE_GOOGLE_US.example_report_partitioned'
    	)
	
wait >> run_gsutil_mv >> load_to_bq_from_gcs >> end
