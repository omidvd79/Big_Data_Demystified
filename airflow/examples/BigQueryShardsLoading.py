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

# Output file for job.
output_file = os.path.join(
    models.Variable.get('gcs_bucket'), 'MyBucket',
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) + os.sep
# Path to GCS buckets. no need to add gs://
DST_BUCKET = ('MyBucket')
 
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



network_table							='MyDataSet.table_shard_'

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


### start & end date = delta period.
## -3 days?
delta=-3 
start_date = datetime.date.today() + datetime.timedelta(delta)
end_date = datetime.date.today()

today_macro='{{ ds_nodash }}'
 
with models.DAG('BigQueryShardsLoading', schedule_interval='@once', default_args=default_dag_args) as dag:

	for single_date in daterange(start_date, end_date):
		load_to_bq_from_gcs_NetworkImpressions = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
    		task_id='load_to_bq_from_gcs_'+single_date.strftime("%Y%m%d"),
    		source_objects=[
            	'my_file_prefix_'+single_date.strftime("%Y%m%d")+'*'
        	],
    		skip_leading_rows=1 ,
    		write_disposition='WRITE_TRUNCATE', #overwrite?
    		create_disposition='CREATE_IF_NEEDED',
    		bucket=DST_BUCKET,
    		destination_project_dataset_table=network_table+single_date.strftime("%Y%m%d"),
    		autodetect='true')

