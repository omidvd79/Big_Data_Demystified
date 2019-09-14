
from airflow.models import DAG
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


import boto3
s3 = boto3.client('s3')


def delete_file_S3(bucket_name, object_name):
          s3.delete_object(Bucket=bucket_name, Key=object_name)

s3r = boto3.resource('s3')
def my_delete_files_S3(bucket_name,pre):
        bucket = s3r.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=pre):
                s3r.Object(bucket.name,obj.key).delete()



with DAG(dag_id='full_athena_example',
         schedule_interval=None,
         start_date=datetime(2019, 5, 21)) as dag:

    run_query = AWSAthenaOperator(
        task_id='run_query',
        query="select * from sampledb.elb_logs",
        output_location='s3://ingestion/output/',
        database='sampledb'
    )
 
    drop_query = AWSAthenaOperator(
        task_id='drop_query',
        query="drop TABLE if exists data_lake_transformation.elb_logs_parquet",
        output_location='s3://transformation/output/',
        database='transformation'
    )
    
    delete_files_S3_task = PythonOperator(
        task_id='delete_files_S3',
        python_callable=my_delete_files_S3,
        op_kwargs={
        'bucket_name': 'transformation',
        'pre': 'elb-logs-parquet/'
        })
    transform_query = AWSAthenaOperator(
        task_id='transform_query',
        query="CREATE TABLE data_lake_transformation.elb_logs_parquet WITH (format = 'PARQUET') AS SELECT * FROM sampledb.elb_logs",
        output_location='s3://transformation/elb-logs-parquet/',
        database='sampledb'
    )

run_query >> drop_query >> delete_files_S3_task >> transform_query