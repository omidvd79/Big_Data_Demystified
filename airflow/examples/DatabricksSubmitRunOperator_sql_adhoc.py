from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from datetime import datetime, timedelta

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'databricks_operator_example',
    default_args=default_args,
    description='An example DAG using the Databricks operator',
    schedule_interval=timedelta(hours=1)
)

# Define the Databricks operator
databricks_operator = DatabricksSubmitRunOperator(
    task_id='databricks_operator_task',
    databricks_conn_id='databricks_default',
    new_cluster={
        'spark_version': '8.4.x-scala2.12',
        'node_type_id': 'i3.xlarge',
        'num_workers': 1
    },
    spark_jar_task={
        'main_class_name': 'com.databricks.example.MyClass',
        'parameters': [
            '--query', 'SELECT * FROM my_table LIMIT 100',
            '--output', 'my_table_output'
        ]
    },
    dag=dag
)

# Define the DAG dependencies
databricks_operator
