from airflow.utils.trigger_rule import TriggerRule
import datetime as dt
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator

dag = DAG(
    dag_id='branching_example',
    schedule_interval='@once',
    start_date=dt.datetime(2019, 2, 28)
)


import datetime
datetime.datetime.today()
#Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
my_date = datetime.datetime.today().weekday()


def weekday_or_weekend_branch():
    if my_date == 5:  # only Saturday we rest
        return 'weekend_task'
    else:
        return 'weekday_task'
    

weekday_task = DummyOperator(task_id='weekday_task', dag=dag)
weekend_task = DummyOperator(task_id='weekend_task', dag=dag)

branch_task = BranchPythonOperator(
    task_id='branching',
    python_callable=weekday_or_weekend_branch,
    dag=dag,
)

branch_task >> weekday_task 
branch_task >> weekend_task





"""
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
"""

