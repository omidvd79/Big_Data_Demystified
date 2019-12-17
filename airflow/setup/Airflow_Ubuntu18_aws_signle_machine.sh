sudo apt-get update

sudo apt-get -y install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev python-setuptools default-libmysqlclient-dev libkrb5-dev libsasl2-dev

sudo apt install -y python3-pip  python-boto3

#any version higher than 2.1.4 will fail as the project is deprecated, 
sudo pip3 install pymssql==2.1.4

sudo pip3 install pystan

sudo pip3 install --upgrade setuptools

sudo pip3 install apache-airflow

sudo -H pip3 install apache-airflow[all_dbs]

sudo -H pip3 install apache-airflow[devel]

sudo pip3 install apache-airflow[all]
