from airflow.utils.trigger_rule import TriggerRule
import datetime as dt
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator

dag = DAG(
    dag_id='conditional_example',
    schedule_interval='@once',
    start_date=dt.datetime(2019, 2, 28)
)

task_start = DummyOperator(
        task_id='task_start',       
        dag=dag)

conditional_task = DummyOperator(
        task_id='conditional_task',        
        dag=dag)

task_failure = DummyOperator(
        task_id='task_failure',       
        trigger_rule=TriggerRule.ALL_FAILED,
        dag=dag)
        
task_follow_failure = DummyOperator(
        task_id='task_follow_failure',       
        trigger_rule=TriggerRule.ALL_SUCCESS,
        dag=dag)

task_success = DummyOperator(
        task_id='task_success',        
        trigger_rule=TriggerRule.ALL_SUCCESS,        
        dag=dag)

cleanup_task = DummyOperator(
        task_id='cleanup_task',
        trigger_rule=TriggerRule.ONE_SUCCESS,
        dag=dag)


conditional_task.set_upstream(task_start)
task_failure.set_upstream(conditional_task)
task_follow_failure.set_upstream(task_failure)
task_success.set_upstream(conditional_task)
cleanup_task.set_upstream(task_failure)
cleanup_task.set_upstream(task_success)