""" 
This DAG relies on three Airflow variables
https://airflow.apache.org/concepts.html#variables
* gcp_project - Google Cloud Project to use for the Cloud Dataproc cluster.
* gce_zone - Google Compute Engine zone where Cloud Dataproc cluster should be
  created.
* gcs_bucket - Google Cloud Storage bucket to use for result of Hadoop job.
  See https://cloud.google.com/storage/docs/creating-buckets for creating a
  bucket.
"""

import datetime
import os
import logging

from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
#from airflow.operators import dummy_operator
from airflow.contrib.operators.dataproc_operator import DataprocClusterScaleOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataProcHiveOperator
from airflow.contrib.operators.dataproc_operator import DataProcSparkSqlOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterDeleteOperator



from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator

# Import operator from plugins
from airflow.contrib.operators import gcs_to_gcs


from airflow.utils import trigger_rule

# Output file for job.
 
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

my_cluster_name='omid-test4'
my_region='us-central1'
my_bucket='omid-eu-west-2' #avoid cross region, this only for testing purposes.
my_instance='n1-highmem-4'
my_disk_size=1024 # for performance purposes.
my_zone='' #default
my_idle_delete_ttl=70000 #  time in seconds to auto delete in case of no destroy_cluster


with models.DAG(
        'dataproc_create_and_destroy_poc',
        schedule_interval='@once', 
        default_args=default_dag_args) as dag:
            
     create_dataproc_cluster = DataprocClusterCreateOperator(
    	task_id='create_dataproc_cluster',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	num_workers=2,
    	storage_bucket=my_bucket,
    	#init_actions_uris='zeppelin',
    	master_machine_type=my_instance,
    	master_disk_size=my_disk_size,
    	worker_machine_type=my_instance,
    	worker_disk_size=my_disk_size,
        num_preemptible_workers=0, #use scale out/in operator
        zone=my_zone,
        idle_delete_ttl=my_idle_delete_ttl,
     	dag=dag)
    
     
     dataproc_scale_out = DataprocClusterScaleOperator(
        task_id='dataproc_scale_out',
        cluster_name=my_cluster_name,
        region=my_region,
        num_workers=2,
        num_preemptible_workers=0,
        graceful_decommission_timeout='1h',
        dag=dag)
      
     dummy_ETL = DummyOperator(task_id='dummy_ETL', dag=dag)
     
     dataproc_scale_in = DataprocClusterScaleOperator(
        task_id='dataproc_scale_in',
        cluster_name=my_cluster_name,
        region=my_region,
        num_workers=2,
        num_preemptible_workers=0,
        graceful_decommission_timeout='1h',
        dag=dag)
    
     delete_dataproc_cluster = DataprocClusterDeleteOperator(
    	task_id='delete_dataproc_cluster',
    	cluster_name=my_cluster_name,
    	region=my_region,
     	dag=dag)
 	
	
create_dataproc_cluster >> dataproc_scale_out  >> dummy_ETL >> dataproc_scale_in >> delete_dataproc_cluster
   
