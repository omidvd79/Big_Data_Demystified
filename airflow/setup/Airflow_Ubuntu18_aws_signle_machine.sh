sudo apt-get update

sudo apt-get -y install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev python-setuptools libmysqlclient-dev

sudo apt install -y python3-pip  python-boto3

pip3 install pystan

sudo pip3 install apache-airflow

sudo -H pip3 install apache-airflow[all_dbs]

sudo -H pip3 install apache-airflow[devel]

sudo pip3 install apache-airflow[all]
#error on setup of kerberos , TBD FIX should good to get started
