from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 24),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'launch_databricks_cluster',
    default_args=default_args,
    description='Launch a Databricks cluster using Airflow',
    schedule_interval=None,
)

cluster_conf = {
    'new_cluster': {
        'spark_version': '7.3.x-scala2.12',
        'node_type_id': 'i3.xlarge',
        'num_workers': 1
    }
}

notebook_task = DatabricksSubmitRunOperator(
    task_id='launch_cluster',
    dag=dag,
    json={
        'notebook_task': {
            'notebook_path': '/path/to/notebook',
            'base_parameters': {'param1': 'value1', 'param2': 'value2'},
            'cluster_spec': cluster_conf
        }
    }
)
