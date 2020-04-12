import datetime
from datetime import timedelta, date
from airflow.models import DAG
from airflow.operators import BashOperator
from airflow.utils import trigger_rule
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2)
}

# change sceduel interval to somtehing that works for you. be advised 200GB disk is recommended.
dag = DAG(
    dag_id='bash_log_clean_up',
    default_args=args,
    schedule_interval='00 03 * * 0'
)

user = 'omid'

airflow_logs_clean_command = 'sudo -u '+user+' rm -r /home/'+user+'/airflow/logs/*'
airflow_logs_clean = BashOperator(
    task_id='airflow_logs_clean',
    retries=0,
    bash_command=airflow_logs_clean_command,
    dag=dag
)


machin_logs_clean_command = 'sudo -u '+user+' rm -r /home/'+user+'/gs_logs/*'
machin_logs_clean = BashOperator(
    task_id='machin_logs_clean',
    retries=0,
    bash_command=airflow_logs_clean_command,
    dag=dag
)


airflow_logs_clean
machine_logs_clean
