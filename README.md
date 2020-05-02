# PyPnbPartKeepr
New Django Version From scratch of PartKeepr
This README would normally document whatever steps are necessary to get your application up and running.

## Installation on Debian like distribution.


### installing needed package
```
sudo apt-get install python-pip python-dev python-virtualenv postgresql libpq-dev postgresql-client
```

### Clone repo
```
git clone -b production https://github.com/pnb990/PyPnbPartKeepr.git
```

### PostgreSql Database configuration

Add password to postgres user for administration of this

```
sudo passwd postgres
```

Connecting to postgres
```
su postgres -c psql
```

Create Database owner partkeeprpsqluser with PartKeeprPsqlPass passwords.
```
CREATE ROLE partkeeprpsqluser PASSWORD 'PartKeeprPsqlPass' LOGIN;
```
it is recommanded to change it but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Then create database partkeeprpsqldb
```
CREATE DATABASE partkeeprpsqldb OWNER 'partkeeprpsqluser';
```
You may change database name but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Exit psql client
```
exit
```

### create virtual environment for this application

Generally you need to create an virtual environment except if you have all needed package listed in requirements.txt

So in top folder of PyPnbPartKeepr, last line is only needed if you want import data from PartKeepr:
```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
cd PyPnbPartKeepr
pip install -r requirements.txt
pip install -r requirements-mysql.txt
```

### create table and admin user

# don't forget if not done yet
```
source venv/bin/activate
cd PyPnbPartKeepr
```

Update database schema
```
python manage.py migrate
```

Create administrator
```
python manage.py createsuperuser
```

### importing old PartKeepr data

To import old database and file use importFromParkKeepr script.

See help with python importFromParkKeepr -h 

exemple:
```
./importFromParkKeepr.py testdb -u TestUser -P TestPass --host 127.0.0.1 -d ../data_old
```



### Some use full command for debug

Before using Django commande don't forget to source django_set_env.sh

```
source ~/django_set_env.sh
```

Apply database migration

```
./manage migrate
```

Create super user

```
./manage.py createsuperuser
```

If you use static files
```
python manage.py collectstatic
```

For debug start :
```
./debug_server.sh
```

### Environment configuration

For easy debug create a file in ~/django_set_env.sh and fill correctly fields:

#!/bin/sh

export EMAIL_HOST='smtp.gmail.com'
export EMAIL_PORT='465'
export EMAIL_USER='xxxx@xxxx.com'
export EMAIL_PASS='xxxxxxxxxxxxx'
export EMAIL_SSL='True'
export EMAIL_TLS='False'

DEBUG=True
DEBUG_TOOLBAR=True
DEBUG_NO_CACHES=True
#ALLOWED_HOSTS=['MyPnbPartKeepr.com']

```

