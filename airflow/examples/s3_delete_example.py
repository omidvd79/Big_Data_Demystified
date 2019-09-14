from airflow.models import DAG
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
from airflow.contrib.operators.s3_delete_objects_operator  import S3DeleteObjectsOperator
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

with DAG(dag_id='s3_delete',
         schedule_interval=None,
         start_date=datetime(2019, 5, 21)) as dag:

    delete_file_S3_task = PythonOperator(
        task_id='delete_file_S3',
        python_callable=delete_file_S3,
        op_kwargs={
        'bucket_name': 'data-lake-ingestion',
        'object_name': 'athena-output/file.csv'
        })
        
       
    delete_files_S3_task = PythonOperator(
        task_id='delete_files_S3',
        python_callable=my_delete_files_S3,
        op_kwargs={
        'bucket_name': 'data-lake-ingestion',
        'pre': 'athena-output2/'
        })

delete_files_S3_task >> delete_file_S3_task
    