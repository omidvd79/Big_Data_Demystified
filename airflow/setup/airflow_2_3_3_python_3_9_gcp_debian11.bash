#assuming GCP debian 1 package
sudo apt-get -y update
sudo apt-get -y install build-essential
#default python is 3.9
sudo apt -y install python3-pip
AIRFLOW_VERSION=2.3.3
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint  https://raw.githubusercontent.com/apache/airflow/constraints-2.3.3/constraints-3.9.txt

#adding google operators (notice it may break due to versining):
pip install apache-airflow-providers-google

#addition to support AWS RDS Aurora
sudo apt-get -y install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient



#manual steps:
#echo "***************************** Manual steps belows************************"
#echo "1. update bashrc to contain path to "export PATH=$PATH:~/.local/bin" via nano ~/.bashrc, add the path, save, and then exit and type "bash".
#echo "2. airflow db init"
#echo "3. create user (example inside the script with in comment"
#echo "4. start airflow web server + scheduler"
#echo "5. make sure GCE firewall is on open on HTTP / HTTPS port 8080"
#example on how to create airflow user.
#airflow users create \
#          --username admin \
#          --firstname FIRST_NAME \
#          --lastname LAST_NAME \
#          --role Admin \
#          --email admin@example.org
