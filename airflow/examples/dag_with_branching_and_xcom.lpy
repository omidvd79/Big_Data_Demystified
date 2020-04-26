import os
import logging
from datetime import timedelta, date
import datetime   

from airflow import DAG
from airflow import models
from airflow.contrib.operators import bigquery_to_gcs
from airflow.contrib.operators import gcs_to_bq
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator
from airflow.contrib.operators import gcs_to_gcs
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.utils import trigger_rule
from airflow.operators import PythonOperator
from airflow.utils import trigger_rule
from airflow.operators.python_operator import BranchPythonOperator


# for insert/select form Aiflow DB
import sqlalchemy as db
engine = db.create_engine('mysql://airflow:airflow@1.2.3.4:3306/airflow')

#####################################

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())


################################
## default args for airflow
################################
default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    'owner': 'Jutomate',    
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

################################
## push dicom to dicom_dedup   #
################################
def insert(input):
	
	## tyring now to insert data
	try:
		conn = engine.connect()
		trans = conn.begin()
		insert_into='INSERT INTO table_name(id,value)  VALUES (\''+id+'\',\'' +input+ '\' );'
		conn.execute(insert_into)
		trans.commit()
		return ("insert input!!!")
	except:
		return ("unable insert ")

######################################
## pull dicom_sha_from airflow db   ##
######################################
def is_contidional_select(input):
	connection = engine.connect()
	metadata = db.MetaData()
	table_name = db.Table('table_name', metadata, autoload=True, autoload_with=engine)

	#table contain
	#1. col_id
	#2. col_value

	#SQL :SELECT min(id) FROM table_name 	
	query = db.select([db.func.min(dicom_dedup.columns.col_id)]).where(dicom_dedup.columns.col_value ==input )

	ResultProxy = connection.execute(query)

	ResultSet = ResultProxy.fetchall()

	#parsing results
	v=[value for value, in ResultSet]
	
	if v[0]: 
		print ("input found")
		return True
	else:
		print ("input not found")
		return False
	


#######################
## conditional logic  #
#######################
def is_contidional(input):
		if is_contidional_select(input):
				return True
		else:
				print( insert(input) )	
				return False	
		

##################################
## conditional fucntion
###################################
def conditional_func(input):
    if is_contidional(input) == True:  # only Saturday we rest
        return 'stop'
    else:
        return 'continue'

with models.DAG(
        'dag_with_branching_and_xcom',
        # Continue to run DAG once per day
        schedule_interval=None,
        default_args=default_dag_args) as dag:

		branching = BranchPythonOperator(task_id='branch',python_callable=conditional_func,op_kwargs={'input': input},dag=dag)
		duumy_stop 			= DummyOperator(task_id='stop')
		dummy_continue 		= DummyOperator(task_id='continue') 
		
