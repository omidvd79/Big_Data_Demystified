** getting started on installing airflow:

1. create a machine in GCP

2. ssh to the machine

3. type the follow:
sudo apt-get git
git clone https://github.com/omidvd79/Big_Data_Demystified.git
cd Big_Data_Demystified/airflow/setup/
sh airflow_2_3_3_python_3_9_gcp_debian11.bash
cp start_airflow.sh ~/
chmod 777 ~/start_airflow.sh
mkdir gs_logs

4. edit the bashrc file to add airflow, add in this line in the end: "export PATH=$PATH:~/.local/bin"

nano ~/.bashrc

5. after you edit the bashrc file - be sure to load basrc in current terminal via cmd:

bash

6. init airflow db via:

airflow db init

7. add airflow users:

airflow users create  --username admin  --firstname FIRST_NAME  --lastname LAST_NAME   --role Admin  --email admin@example.org

8. make sure port 8080 is open in the machine to your IP:

9. start airflow using our bash script (be sure to understand the script):

sh ~/start_airflow.sh

10. for Local Executor , install CloudSQL MySQL seperatly (1 CPI, 3.75 RAM, 10GD SSD, Private LAN+ PUBLIC LAN) , dont forget to the flag: 

explicit_defaults_for_timestamp=1

11. in airflow.cfg replace the sql_alchemy_conn connection to:

sql_alchemy_conn = mysql://{USERNAME}:{PASSWORD}@{MYSQL_PRIVATE_IP}:3306/airflow


 



