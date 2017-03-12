- setup a local developing environment with hadoop-vagrant
-- follow the guide to install the prerequisites (https://github.com/python279/hadoop-vagrant)
-- startup one ubuntu14.4 vm
```
$ cd ubuntu14.4
$ vagrant up u1401
$ vagrant ssh u1401
$ get -c https://repo.continuum.io/archive/Anaconda2-4.3.0-Linux-x86_64.sh && bash Anaconda2-4.3.0-Linux-x86_64.sh
$ which python
/home/vagrant/anaconda2/bin/python
$ conda install django pyserial
$ pip install apscheduler
$ sudo apt-get install -y git
$ cd /vagrant
$ git clone git@github.com:python279/pyairmonitor.git
$ sudo apt-get install -y mysql-server
$ mysql -u root -p
mysql> CREATE DATABASE pyairmonitor;
mysql> CREATE USER 'pyairmonitor'@'%' IDENTIFIED BY 'pyairmonitor';
mysql> GRANT ALL ON pyairmonitor.* TO 'pyairmonitor'@'%';
mysql> FLUSH PRIVILEGES;
mysql> USE pyairmonitor;
mysql> SOURCE pyairmonitor/database/pyairmonitor.sql;
mysql> EXIT;

$ cd pyairmonitor/server
$ python manage.py runserver 0.0.0.0:8080 &

-- run client as a simulator on your laptop
```
$ pip install apscheduler pyserial
$ cd pyairmonitor/client
$ python Client.py -s
```

-- run client as the real sensor PMS5003T on your laptop
```
$ pip install apscheduler pyserial
$ cd pyairmonitor/client
$ python Client.py
```

-- run client as the real sensor PMS5003T on raspberry pi 3
```
$ ssh pi@raspberry_ip
$ sudo su -
$ pip install virtualenv
$ virtualenv pyairmonitor
$ source pyairmonitor/bin/activate
$ pip install apscheduler pyserial
$ ssh-keygen -t rsa -C "my raspberry pi"
$ cat .ssh/id_rsa.pub
$ mkdir src; cd src; git clone git@github.com:python279/pyairmonitor.git
$ cd src/pyairmonitor
$ python Client.py
```

