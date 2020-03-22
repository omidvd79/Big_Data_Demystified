from builtins import range
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='Big_Data_Demystfied_BashOperator_sudo_imporsenation_example',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=['example']
)

first_run = BashOperator(
    task_id='first_run',
    bash_command='echo "hello"',
    dag=dag,
)

second_bash = BashOperator(
    task_id='second_run',
    bash_command='sudo -u omid touch /home/omid/file.txt',
    dag=dag,
)

second_bash << first_run
