from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators import PythonOperator
import pprint

args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG('example_xcom_v3', schedule_interval=None, default_args=args, tags=['example'])

def pusher(**kwargs):
	base= kwargs['ti'].xcom_pull(key=None, task_ids='push_1')
	if (base is not None):
		kwargs['ti'].xcom_push(key='value from pusher ', value=int(base)+1 )
	else:

		kwargs['ti'].xcom_push(key='value from pusher ', value=1  )

def puller(**kwargs):
	"""Pull all previously pushed XComs and check if the pushed values match the pulled values."""
	ti = kwargs['ti']
	# get value_1
	pulled_value_1 = ti.xcom_pull(key=None, task_ids='push_1')
	print (pulled_value_1)
	



def pusher_dynamic(my_task_id, **kwargs):
	#print(ds)
	print("pushing| my task id: "+str(my_task_id)+" Notice, the task operator id is also pushed, imliciltly")
	print(kwargs)
	print(kwargs['ti'])
	kwargs['ti'].xcom_push(key='value from pusher dynamic', value=int(my_task_id) )
	return 'Whatever you return gets printed in the logs'

def puller_dynamic(my_task_id,**kwargs):
        ti = kwargs['ti']
        pulled_value = ti.xcom_pull(key='value from pusher dynamic', task_ids='push_'+str(my_task_id) )
        print ("pulled value based on pusher_id: " +str(pulled_value))

i=1
push1 = PythonOperator(task_id='push_1',	provide_context=True,dag=dag,python_callable=pusher)
pull1 = PythonOperator(task_id='pull_1',	provide_context=True,dag=dag,python_callable=puller)

#notice I am pulling based on push_1 id, expeted value to push is 2, for pull is1,  b/c we are sending the push_1 id...
i=i+1
push2 = PythonOperator(task_id='push_2', 	provide_context=True,dag=dag,python_callable=pusher)
pull2 = PythonOperator(task_id='pull_2',       	provide_context=True,dag=dag,python_callable=puller)



#trying to create a dynamic pusher called pusher_synami, accpeting a counter  and pushes it to the MySQL 
i=i+1
my_task_id=i
push3 = PythonOperator(task_id='push_'+str(i),        provide_context=True,python_callable=pusher_dynamic,op_kwargs={'my_task_id': my_task_id},dag=dag)
pull3 = PythonOperator(task_id='pull_'+str(i),        provide_context=True,python_callable=puller_dynamic,op_kwargs={'my_task_id': my_task_id},dag=dag)

i=i+1
my_task_id=i
push4 = PythonOperator(task_id='push_'+str(i),        provide_context=True,python_callable=pusher_dynamic,op_kwargs={'my_task_id': my_task_id},dag=dag)
pull4 = PythonOperator(task_id='pull_'+str(i),        provide_context=True,python_callable=puller_dynamic,op_kwargs={'my_task_id': my_task_id},dag=dag)

push1 >> pull1 >> push2 >> pull2 >> push3 >> pull3 >> push4 >> pull4
