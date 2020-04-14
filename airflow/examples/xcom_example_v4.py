from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators import PythonOperator
from airflow.operators.bash_operator import BashOperator


args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

dag = DAG('example_xcom_v4', schedule_interval=None, default_args=args, tags=['example'])

t1 = BashOperator(
    task_id="t1",
    bash_command='echo "{{ ti.xcom_push(key="k1", value="v1") }}" "{{ti.xcom_push(key="k2", value="v2") }}"',
    dag=dag,
)

t2 = BashOperator(
    task_id="t2",
    bash_command='echo "{{ ti.xcom_pull(key="k1") }}" "{{ ti.xcom_pull(key="k2") }}"',
    dag=dag,
)

t1 >> t2
