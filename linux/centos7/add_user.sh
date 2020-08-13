# add user cento7

sudo adduser sqream
sudo usermod -aG root sqream
yum install -y nano

#https://phoenixnap.com/kb/how-to-create-add-sudo-user-centos
#sudo nano /etc/ssh/sshd_config
#AllowUsers sqream - do not use this. this will not let u login to the machine and cause problems....
#sudo systemctl restart sshd

# add user to sudoers
# https://phoenixnap.com/kb/how-to-create-add-sudo-user-centos
# nano /etc/sudoers
# sqream ALL=(ALL)        ALL

#change password for user
passwd sqream

