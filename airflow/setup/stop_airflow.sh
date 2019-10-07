echo tyring to stop Aiflow
pkill airflow
echo trying to restart  airflow scheudler
airflow scheduler -D
