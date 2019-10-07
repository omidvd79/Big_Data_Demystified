echo staring AirflowServer
nohup airflow webserver $* > ~/gs_logs/webserver.logs &
echo starting Airflow Scheduler
nohup airflow scheduler > ~/gs_logs/scheduler.logs &
echo list PID of ariflow
ps -eaf | grep airflow
