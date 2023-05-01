from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime, timedelta

# Define the DAG
default_args = {
    'owner': 'Jutomate',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'DatabricksSubmitRunOperator_sql_example',
    default_args=default_args,
    description='DatabricksSubmitRunOperator',
    schedule_interval=None
)

# Define the Databricks operator
databricks_operator = DatabricksSubmitRunOperator(
    task_id='databricks_operator_task',
    databricks_conn_id='databricks_default',
    new_cluster={
        'spark_version': '7.3.x-scala2.12',
        'node_type_id': 'n1-standard-4',#assuming GCP instances
        'num_workers': 1
    },
    spark_jar_task={
        'main_class_name': 'com.databricks.example.MyClass',
        'parameters': [
            '--query', 'SELECT * FROM my_table LIMIT 100',
            '--output', 'my_table_output'
        ],
    },
    libraries=[{"jar": "dbfs:/jutomate/job1.jar"}],
    dag=dag
)

# Define the DAG dependencies
databricks_operator
