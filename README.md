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

copy PyPnbPartKeepr-dist.conf.yaml in PyPnbPartKeepr.conf.yaml or /etc/PyPnbPartKeepr.conf.yaml and update value.
```
cp PyPnbPartKeepr-dist.conf.yaml PyPnbPartKeepr.conf.yaml
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

and for reverse proxy:
```
    <Location "/PnbPartKeepr">
        Require all granted

        ProxyPass "http://localhost:83/PnbPartKeepr/"
        ProxyPassReverse http://127.0.0.1:83/PnbPartKeepr/

        ProxyPreserveHost On
        RequestHeader set X-Forwarded-Proto "https"
        RequestHeader set X-Forwarded-Host  "btvangers.no-ip.org"
        RequestHeader set X-Forwarded-Port  "443"

    </Location>
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

### Upgrade

Use upgrade.sh or follow command below
```
sudo service bdws_systemd_venv stop
git pull
git submodule update --init --recursive
export PIPENV_VENV_IN_PROJECT=1
pipenv install
pipenv run ./manage.py migrate
pipenv run ./manage.py collectstatic
sudo systemctl daemon-reload
sudo service bdws_systemd_venv start
```

### Backup

Create a backup, in python environment:

```
pipenv run ./manage.py dbbackup --clean
pipenv run ./manage.py mediabackup --clean
```

To automatise backup put in crontab the line below
```
 27    40      5       *       *       *       /usr/local/bdws/bdws_serverpy/backup.sh
```

### Restore

Check in /etc/postgresql/x/main/postgresql.conf that below lines are same as backup server.
'''
lc_messages = 'fr_FR.UTF-8'
lc_monetary = 'fr_FR.UTF-8'
lc_numeric = 'fr_FR.UTF-8'
lc_time = 'fr_FR.UTF-8'
'''
and check this page for help https://www.shubhamdipt.com/blog/how-to-change-postgresql-database-encoding-to-utf8/

Clean up database:
```bash
su postgres -c psql
```

Drop and create new empty database
```
DROP DATABASE bdwspsqldb; CREATE DATABASE bdwspsqldb OWNER 'bdwspsqluser';
```

Check encoding 'UTF8' with '\l' command
```
    Name    |    Owner     | Encoding  | Collate | Ctype | ICU Locale | Locale Provider |   Access privileges
------------+--------------+-----------+---------+-------+------------+-----------------+-----------------------
 bdwspsqldb | bdwspsqluser | UTF8      | C       | C     |            | libc            |
```

Exit pg client
```
exit
```

Restore a backup, in python environment:

Before check 'BACKUP_DIR' in configuration files
then create a temp directory inside

If database is not setted:
```bash
pipenv run ./manage.py migrate # if database was just created
pipenv run ./manage.py dbrestore -I [backup_file.psql]
pipenv run ./manage.py mediarestore -I [backup_file.tar]
pipenv run ./manage.py collectstatic
```
if some data not works (too long ... ), edit file and retry... :(

### restore in devcontainer

```bash
docker cp backup.psql.bin my_devcontainer-db-1:/tmp/
docker exec -it my_devcontainer-db-1 \
    pg_restore \
        --dbname=postgresql://partkeeprpsqluser@db:5432/partkeeprpsqldb \
        --single-transaction --clean --if-exists \
        /tmp/backup.psql.bin
```

