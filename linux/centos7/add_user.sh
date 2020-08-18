# add user cento7

sudo adduser sqream
sudo usermod -aG root sqream
yum install -y nano

# add user to sudoers
# https://phoenixnap.com/kb/how-to-create-add-sudo-user-centos
# nano /etc/sudoers
# sqream ALL=(ALL)        ALL

#change password for user
#passwd sqream

