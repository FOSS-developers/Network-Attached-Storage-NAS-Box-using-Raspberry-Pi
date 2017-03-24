#!/usr/bin/python

import os
os.system("sudo apt-get update")
os.system("sudo apt-get upgrade -y")
os.system("sudo apt-get install python-pip -y")
os.system("sudo apt-get install python-opencv -y")
os.system("sudo apt-get install mariadb-server -y")
os.system("sudo apt-get install python-mysql.connector -y")
os.system("sudo apt-get install apache2 -y")
os.system("sudo apt-get install samba samba-common-bin -y")
os.system("sudo apt-get install pure-ftpd -y")
os.system("sudo pip install flask")
os.system("sudo pip install flask-mail")
os.system("echo -e \"\ny\ny\nroot\nroot\ny\nn\nn\ny\" | mysql_secure_installation")
os.system("echo \"Enter MariaDb database password for root user(i.e. root)!!!\" ")
os.system("sudo mysql -u root -p -e \"create database nas\" ")
os.system("mysql -u root -p nas < nas.dump")
os.system("echo \"Initial setup Successful! \" ")
