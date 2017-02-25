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
$ conda install django
$ sudo apt-get install mysql-server
$ mysql -u root -p
mysql> CREATE DATABASE pyairmonitor;
mysql> CREATE USER 'pyairmonitor'@'%' IDENTIFIED BY 'pyairmonitor';
mysql> GRANT ALL ON pyairmonitor.* TO 'pyairmonitor'@'%';
mysql> FLUSH PRIVILEGES;
mysql> exit;
$
```

