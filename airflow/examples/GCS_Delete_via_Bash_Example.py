from airflow.models import DAG
import datetime as dt
from airflow.operators import BashOperator

dag = DAG(
    dag_id='GCS_Delete_via_Bash_Example',
    schedule_interval='@once',
    start_date=dt.datetime(2019, 2, 28)
)

GCS_Delete_via_Bash_Example = BashOperator(
        task_id='GCS_Delete_via_Bash_Example', 
        bash_command='gsutil rm -r gs://data_lake_ingestion_us/dfp_data_transfer_impressions_unified_parquet/*',      
        dag=dag)
        
GCS_Delete_via_Bash_Example



