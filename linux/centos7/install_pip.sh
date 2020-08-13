#install pip centos
#https://www.liquidweb.com/kb/how-to-install-pip-on-centos-7/
sudo yum install -y epel-release
sudo yum -y update
sudo yum -y install python-pip
sudo pip install --upgrade pip
pip install --upgrade setuptools
sudo yum install --assumeyes python3-pip
pip3 install --upgrade setuptools




