sudo apt-get -y update
sudo apt-get -y install build-essential
#default python is 3.8.5
sudo apt -y install python3-pip
AIRFLOW_VERSION=1.10.14
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint  https://raw.githubusercontent.com/apache/airflow/constraints-1.10.14/constraints-3.8.txt
echo "update bashrc to contain path to PATH=$PATH:~/.local/bin"

