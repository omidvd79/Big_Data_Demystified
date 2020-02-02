from __future__ import print_function
from builtins import range
from airflow.operators import PythonOperator
from airflow.models import DAG
from datetime import datetime, timedelta

import datetime
import os
import logging

from airflow import DAG
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator
from airflow.contrib.operators import gcs_to_bq

import time
from pprint import pprint




today_date = datetime.datetime.now().strftime("%Y%m%d")


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

with DAG(dag_id='monitor_dag', schedule_interval=None, default_args=default_dag_args) as dag:

	bash_prerequisites_install_cmd="""sudo apt install -y python-pip"""
	bash_prerequisites_install = BashOperator(task_id='bash_prerequisites_install', bash_command=bash_prerequisites_install_cmd)
    
	bash_pip_install_cmd="""sudo pip install pandas google-colab google-cloud-bigquery google-cloud-bigquery-storage pyarrow pyTelegramBotAPI"""
	bash_pip_install = BashOperator(task_id='bash_pip_install', bash_command=bash_pip_install_cmd)

	bash_colab_export_script_cmd="""python /home/omid/gs_dags/script.py"""
	bash_colab_export_scriptTask = BashOperator(task_id='bash_colab_export_script', bash_command=bash_colab_export_script_cmd)	

bash_prerequisites_install  >> bash_pip_install >>  bash_colab_export_scriptTask
