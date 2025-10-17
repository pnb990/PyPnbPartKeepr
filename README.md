# PyPnbPartKeepr
New Django Version From scratch of PartKeepr
This README would normally document whatever steps are necessary to get your application up and running.

## Installation on Debian like distribution.


### installing needed package
```
sudo apt-get install pipenv postgresql postgresql-client
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
it is recommended to change it but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Then create database partkeeprpsqldb
```
CREATE DATABASE partkeeprpsqldb OWNER 'partkeeprpsqluser';
```
You may change database name but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Exit psql client
```
\q
```

### create virtual environment for this application

Generally you need to create an virtual environment except if you have all needed package listed in requirements.txt

So in folder of PyPnbPartKeepr, last line is only needed if you want import data from PartKeepr:
```bash
export PIPENV_VENV_IN_PROJECT=1 # optional and don't forget later
cd PyPnbPartKeepr
pipenv install
```
or for development version
```bash
pipenv install --dev
```

### create table and admin user

copy PyPnbPartKeepr-dist.conf.json in PyPnbPartKeepr.conf.json or /etc/PyPnbPartKeepr.conf.json and update value.
```
copy PyPnbPartKeepr-dist.conf.json PyPnbPartKeepr.conf.json
```

Update database schema
```
pipenv run python manage.py migrate
```

Create administrator
```
pipenv run python manage.py createsuperuser
```

each time you change static files need to do this:
```
pipenv run python manage.py collectstatic
```


### importing old PartKeepr data

To import old database and file use importFromParkKeepr script.

See help with python importFromParkKeepr -h

exemple:
```
./importFromParkKeepr.py testdb -u TestUser -P TestPass --host 127.0.0.1 -d ../data_old
```

### Apache configuration

First in addition to allow reading, you need to allow writing in media folder:
```
setfacl -R -m u:www-data:rwX media
setfacl -R -m d:u:www-data:rwX media
```

#### with gunicon
```
pip install -d
```
create symbolic link of pnbpartkeepr_systemd_venv.service in 
/etc/systemd/system/

#### mode 1 not best one
copy site-PyPnbPartKeepr.conf file into /etc/apache2/sites-available/PyPnbPartKeepr.conf

allow apache access 
```
setfacl -R -m u:www-data:rX .
setfacl -R -m d:u:www-data:rX .
setfacl -R -m u:www-data:rwX media
setfacl -R -m d:u:www-data:rwX media
```

then install apache WSGI
```
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo a2ensite site-PyPnbPartKeepr.conf
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

