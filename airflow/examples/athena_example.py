
from airflow.models import DAG
from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
from datetime import datetime

with DAG(dag_id='simple_athena_query',
         schedule_interval=None,
         start_date=datetime(2019, 5, 21)) as dag:

    run_query = AWSAthenaOperator(
        task_id='run_query',
        query="select * from sampledb.elb_logs",
        output_location='s3://ingestion/athena-output/',
        database='sampledb'
    )
 
    drop_query = AWSAthenaOperator(
        task_id='drop_query',
        query="drop TABLE if exists data_lake_transformation.elb_logs_parquet",
        output_location='s3://tranformation/athena-output/',
        database='data_lake_transformation'
    )
    
    transform_query = AWSAthenaOperator(
        task_id='transform_query',
        query="CREATE TABLE data_lake_transformation.elb_logs_parquet WITH (format = 'PARQUET') AS SELECT * FROM $
        output_location='s3://tranformation/athena-output/',
        database='sampledb'
    )

run_query >> drop_query >> transform_query
