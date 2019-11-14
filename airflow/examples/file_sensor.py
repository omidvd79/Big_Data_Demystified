from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dummy_operator    import DummyOperator
from airflow.contrib.sensors.gcs_sensor  import GoogleCloudStorageObjectSensor
import datetime
from datetime import date, timedelta
import airflow

default_args = {
    "depends_on_past" : False,
    "start_date"      : airflow.utils.dates.days_ago( 1 ),
    "retries"         : 1,
    "retry_delay"     : datetime.timedelta( hours= 5 ),
}

today = datetime.datetime.today() 
yesterday = date.today() - timedelta(days=1)
 #print ('Current date and time:', d)
 
# Converting date into YYYY-MM-DD format
#print(d.strftime('%Y-%m-%d'))

#we need yesterday and today date formats, but prefix and suffix are the same in our example.
file_prefix="myPrefiex/"
file_suffix="_file.csv"

file_date=today.strftime('%Y-%m-%d')
full_path_today=file_prefix+file_date+file_suffix

file_date_yesterday=yesterday.strftime('%Y-%m-%d')
full_path_yesterday=file_prefix+file_date_yesterday+file_suffix


with airflow.DAG( "file_sensor_example", default_args= default_args, schedule_interval= "@once"  ) as dag:

    start_task  = DummyOperator(  task_id= "start" )
    stop_task   = DummyOperator(  task_id= "stop"  )
    sensor_task = FileSensor( task_id= "file_sensor_task", poke_interval= 30,  filepath= "/tmp/" )
    #we expect yesterday to exist
    gcs_file_sensor_yesterday = GoogleCloudStorageObjectSensor(task_id='gcs_file_sensor_yesterday_task',bucket='myBucketName',object=full_path_yesterday)
    #for this example we expect today not to exist, keep running until 120 timeout, checkout docs for more options like mode  and soft_fail
    gcs_file_sensor_today = GoogleCloudStorageObjectSensor(task_id='gcs_file_sensor_today_task',bucket='myBucketName',object=full_path_today, timeout=120)
  

start_task >> sensor_task  >> gcs_file_sensor_yesterday >> gcs_file_sensor_today >> stop_task
