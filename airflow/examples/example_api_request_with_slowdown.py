import datetime
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.trigger_rule import TriggerRule

myList=["api1","api2","api3","api4","api5","api6"]

with DAG(
    dag_id='mixpanel_ingestion2',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) as dag: 
	start = DummyOperator(task_id='start',dag=dag) 
	end = DummyOperator(task_id='end',dag=dag) 

	num_rows = 2
	dummy_count = 1
	rows_count = 0
	dummy_prev = DummyOperator(task_id=f'dummy_{dummy_count-1}', trigger_rule=TriggerRule.ALL_DONE, dag=dag)
	dummy_after = DummyOperator(task_id=f'dummy_{dummy_count}', trigger_rule=TriggerRule.ALL_DONE, dag=dag)
	start >> dummy_prev

	for request in myList:
     	# SET VARIABLE SELLER
		omid = DummyOperator(task_id=f'omid-{request}',dag=dag)
		if rows_count == num_rows:
			rows_count = 0
			dummy_count += 1
			dummy_prev = dummy_after
			dummy_after = DummyOperator(task_id=f'dummy_{dummy_count}', trigger_rule=TriggerRule.ALL_DONE, dag=dag)
		dummy_prev >> omid  >> dummy_after
		rows_count += 1
dummy_after >> end
