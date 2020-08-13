#install python 3.7
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel wget
cd ~/
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar xzf Python-3.7.2.tgz
cd Python-3.7.2.tgz
./configure --enable-optimizations
sudo make altinstall

python3.7 -V
