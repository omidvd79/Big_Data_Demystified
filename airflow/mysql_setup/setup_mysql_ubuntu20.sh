sudo apt update
sudo apt install mysql-server
# wizrad
#sudo mysql_secure_installation
# https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
# https://linuxconfig.org/install-mysql-on-ubuntu-20-04-lts-linux
sudo ufw allow from any to any port 3306 proto tcp

#mysql client
# 
#SET GLOBAL validate_password.policy=LOW;
#CREATE USER 'airflow'@'%' IDENTIFIED BY 'airflow';
#CREATE DATABASE airflow;
#GRANT ALL PRIVILEGES ON airflow.* TO 'airflow'@'%';

