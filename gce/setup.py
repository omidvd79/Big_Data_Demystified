# pip
sudo apt update
sudo apt install -y python-pip
sudo apt install -y python3-pip

# pip packges:
pip install google-cloud


# GCS fuse
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update 
sudo apt-get install -y gcsfuse
