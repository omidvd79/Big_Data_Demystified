import datetime
import os
import logging

from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
from airflow.operators import dummy_operator
#from airflow.operators import BashOperator

# Import operator from plugins
from airflow.contrib.operators import gcs_to_gcs


from airflow.utils import trigger_rule

# Output file for job.
output_file = os.path.join(
    models.Variable.get('gcs_bucket'), 'android_reviews_file_transfer',
    datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) + os.sep
# Path to GCS buckets. no need to add gs://
DST_BUCKET = ('pubsite_prod_rev_ingestion/reviews')
DST_BUCKET_UTF8 = ('pubsite_prod_rev_ingestion/reviews_utf8')

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

with models.DAG(
        'android_reviews_load_to_bigQuery',
        # Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

        
     #load from local bucket o GCS table of android
     logging.error('trying to GCS_TO_BQ: ')
     load_to_bq_from_gcs = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
    	task_id='load_to_bq_from_gcs',
    	source_objects='*',
    	skip_leading_rows=1,
    	write_disposition='WRITE_TRUNCATE', #overwrite?
    	bucket=DST_BUCKET_UTF8,
    	destination_project_dataset_table='DATA.Replica_android_review'
    )
    
    # Define DAG dependencies.
    #create_dataproc_cluster >> run_dataproc_hadoop >> delete_dataproc_cluster
	
	
load_to_bq_from_gcs
   
