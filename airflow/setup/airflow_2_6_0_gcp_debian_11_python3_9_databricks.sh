#####################################
#full manual:
#https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html
####################################

#assuming GCP debian 11 package
sudo apt-get -y update
sudo apt-get -y install build-essential
#default python is 3.9
sudo apt -y install python3-pip
export AIRFLOW_VERSION=2.6.0
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint  https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.8.txt   
# if you want v 2.9.3
#pip install "apache-airflow[celery]==2.9.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.8.txt" --break-system-packages


#adding google operators (notice it may break due to versining):
pip install apache-airflow-providers-google   
#pip install apache-airflow-providers-google   --break-system-packages

#addition to support AWS RDS Aurora
sudo apt-get -y install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient  

#addition to databricks
pip install  apache-airflow-providers-databricks


#add airflow dags folder 
mkdir -p ~/airflow/dags   
mkdir -p ~/gs_logs/

echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
airflow db init

#manual steps:
#echo "***************************** Manual steps belows************************"
#echo "1. update bashrc to contain path to "export PATH=$PATH:~/.local/bin" via nano ~/.bashrc, add the path, save, and then exit and type "bash".
#echo "2. airflow db init"
#echo "3. create user (example inside the script with in comment"
#echo "4. start airflow web server + scheduler"
#echo "5. make sure GCE firewall is on open on HTTP / HTTPS port 8080"
#example on how to create airflow user.
#echo 6: setup configuration: sql_alchemy_conn = mysql://{USERNAME}:{PASSWORD}@{MYSQL_HOST}:3306/airflow
#echo 7: open port 8080 to your IP
#airflow users create --username admin --firstname FIRST_NAME --lastname LAST_NAME --role Admin --email admin@example.org
