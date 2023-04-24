from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksCreateClusterOperator, DatabricksDeleteClusterOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 24),
}

dag = DAG(
    'launch_and_delete_databricks_cluster',
    default_args=default_args,
    description='Launch a Databricks cluster using Airflow and delete it after an hour',
    schedule_interval=None,
)

cluster_config = {
    'spark_version': '7.3.x-scala2.12',
    'node_type_id': 'i3.xlarge',
    'num_workers': 1
}

launch_cluster = DatabricksCreateClusterOperator(
    task_id='launch_cluster',
    dag=dag,
    new_cluster=cluster_config,
)

delete_cluster = DatabricksDeleteClusterOperator(
    task_id='delete_cluster',
    dag=dag,
    cluster_id="{{ task_instance.xcom_pull(task_ids='launch_cluster', key='return_value')['cluster_id'] }}",
    trigger_rule='all_done',
)

launch_cluster >> delete_cluster

# Automatically delete the cluster after 1 hour
dag_timeout = timedelta(hours=1)
dag.default_args['dagrun_timeout'] = dag_timeout
