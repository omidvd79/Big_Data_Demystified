import airflow
import datetime as dt
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.slack_operator import SlackAPIPostOperator


dag = DAG(
    dag_id='example_slack',
    schedule_interval='@once',
    start_date=dt.datetime(2019, 2, 28)
)



def slack_success_task(context):  
    success_alert = SlackAPIPostOperator(
        task_id='slack_success',
        channel="#data",
        token="MySlackApi",
        text = ':red_circle: Airflow Task Success',
        username = 'airflow',)
    return success_alert.execute(context=context)


bash_success_task = BashOperator(
    task_id='bash_success_task',
    bash_command='exit 0',
    on_success_callback=slack_success_task,
    dag=dag)


bash_success_task 
