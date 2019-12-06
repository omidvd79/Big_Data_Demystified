import datetime
import os
import logging

from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
#from airflow.operators import dummy_operator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
 
from airflow.contrib.operators.dataproc_operator import DataprocClusterScaleOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataProcHiveOperator
from airflow.contrib.operators.dataproc_operator import DataProcSparkSqlOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterDeleteOperator

# available from v1.10
#from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
#from airflow.contrib.operators import gcs_delete_operator 
   
from airflow.utils.trigger_rule import TriggerRule

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator

# Import operator from plugins
from airflow.contrib.operators import gcs_to_gcs


from airflow.utils import trigger_rule

# Output file for job.

my_cluster_name='omid-prod4'
my_region='us-central1'
my_bucket='omid-eu-west-2' #avoid cross region, this only for testing purposes.
my_instance='n1-highmem-8'
num_preemptible_vms=360
my_disk_size=1024 # for performance purposes.
my_zone='' #default
my_idle_delete_ttl=70000 #  time in seconds to auto delete in case of no destroy_cluster
DST_BUCKET = ('data_lake_ingestion_us/dfp_data_transfer_impressions_unified_parquet2')
transformation_table_name='DATA_LAKE_TRANSFORMATION_US.dfp_data_transfer_unified_impressions_from_hadoop'
 
 
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




#repartition by date 
# the date time is not in valid format.

insert_overwrite_with_transformation_query="""
set hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE  table_parquet  partition (dt)
select 
* from table """




with models.DAG( 
        'dfp_data_transfer_unified_impressions_from_hadoop5',
        schedule_interval='@once', 
        #schedule_interval='@once', 
        default_args=default_dag_args) as dag:
     
     # insert overwrite is not working via sparkSQL, and the file file is not working in Hive
     # GoogleCloudStorageDeleteOperator will only be supported in v.1.10
     
     
     create_dataproc_cluster = DataprocClusterCreateOperator(
    	task_id='create_dataproc_cluster',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	num_workers=2,
    	storage_bucket=my_bucket,
    	master_machine_type=my_instance,
    	master_disk_size=my_disk_size,
    	worker_machine_type=my_instance,
    	worker_disk_size=my_disk_size,
        num_preemptible_workers=0, #use scale out/in operator
        zone=my_zone,
        idle_delete_ttl=my_idle_delete_ttl,
     	dag=dag)       
     	
     drop_if_exists_src_table = DataProcHiveOperator(
    	task_id='drop_if_exists_src_table',
    	job_name='drop_if_exists_src_table_job_name',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	query=drop_if_exists_src_table
     )
     
     drop_if_exists_dst_table = DataProcHiveOperator(
    	task_id='drop_if_exists_dst_table',
    	job_name='drop_if_exists_dst_table_job_name',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	query=drop_if_exists_dst_table
     )
     
     create_external_src_table = DataProcHiveOperator(
    	task_id='create_external_src_table',
    	job_name='create_external_src_table_job_name',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	query=create_external_src_table
     )
     
     create_external_dst_table = DataProcHiveOperator(
    	task_id='create_external_dst_table',
    	job_name='create_external_dst_table_job_name',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	query=create_external_dst_table
     )
     
     dataproc_scale_out = DataprocClusterScaleOperator(
        task_id='dataproc_scale_out',
        cluster_name=my_cluster_name,
    	region=my_region,
        num_workers=2,
        num_preemptible_workers=num_preemptible_vms,
        graceful_decommission_timeout='1h',
        dag=dag)
      
  
        
     ##notice the insert overwrite was concatenated with set_dynamic_partitions check variable: insert_overwrite_with_transformation_query
     insert_overwrite_with_transformation_query = DataProcSparkSqlOperator(
    	task_id='insert_overwrite_with_transformation_query',
    	job_name='insert_overwrite_with_transformation_query_job_name',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	query=insert_overwrite_with_transformation_query  
    	#query=evya_query  # for dev purposes, dummy query
     )
     
     delete_dataproc_cluster = DataprocClusterDeleteOperator(
    	task_id='delete_dataproc_cluster',
    	cluster_name=my_cluster_name,
    	region=my_region,
    	trigger_rule=TriggerRule.ONE_SUCCESS, #assuming queries will will fail.
    	dag=dag)
    
 create_dataproc_cluster >> drop_if_exists_src_table >> drop_if_exists_dst_table >> create_external_src_table >> create_external_dst_table >> dataproc_scale_out  >> insert_overwrite_with_transformation_query >> delete_dataproc_cluster  
   
