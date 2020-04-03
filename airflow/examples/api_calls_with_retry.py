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
    'retry_exponential_backoff': True,
    'max_retry_delay': datetime.timedelta(minutes=20),
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


with models.DAG(
        'ver5_api_call_with_retry',
        # Continue to run DAG once per day
        schedule_interval="0 3 * * *",
        default_args=default_dag_args) as dag:

	start = DummyOperator(task_id='start')

	end = DummyOperator(task_id='end',trigger_rule="all_done")


	#notice if delta has to be negative, -3 or lower,  so will have some dates in date range - you wont have an operator.
 
	for single_date in daterange(start_date, end_date):
	 
			temp_date=single_date.strftime("%Y-%m-%d")
			day_after_single_date=single_date+ datetime.timedelta(days = 1)
			day_after_single_date=day_after_single_date.strftime("%Y-%m-%d")

			##notice trigger_rule="all_done'
			run_report_remotly_status = BashOperator(task_id='run_report_remotly_'+temp_date,retries=2,retry_delay=datetime.timedelta(seconds=30),retry_exponential_backoff=True,max_retry_delay=datetime.timedelta(minutes=20),bash_command=bash_run_report_remotly_cmd,trigger_rule="all_done")
			start >>  run_report_remotly_status >> end
