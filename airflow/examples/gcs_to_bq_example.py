from builtins import range
from datetime import timedelta
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.contrib.operators import gcs_to_bq


args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='Big_Data_Demystified_gcs_to_bq_example',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=['example']
)


gcs2bq=gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
    task_id='Big_Data_Demystified_gcs2bq',
    bucket='MyBucket',
    source_objects='*',
    destination_project_dataset_table='MyDataSet.MyTable',
    skip_leading_rows=1,
    default_args=args,
    dag=dag
)
