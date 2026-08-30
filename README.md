<!--
SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville  <pnb990@gmail.com>

SPDX-License-Identifier: BSD-3-Clause
-->

# PyPnbPartKeepr
New Django Version From scratch of PartKeepr
This README would normally document whatever steps are necessary to get your application up and running.

## Installation on Debian like distribution.


### installing needed package
```bash
sudo apt-get install postgresql postgresql-client
```

### Clone repo
```bash
git clone -b production https://github.com/pnb990/PyPnbPartKeepr.git
```

### PostgreSql Database configuration

Add password to postgres user for administration of this

if you not yet created psql user password.
```bash
sudo passwd postgres
```

Connecting to postgres
```bash
su postgres -c psql
```

Create Database owner partkeeprpsqluser with PartKeeprPsqlPass passwords.
```
CREATE ROLE partkeeprpsqluser PASSWORD 'PartKeeprPsqlPass' LOGIN;
```
or if already exist
```
ALTER USER partkeeprpsqluser WITH PASSWORD 'PartKeeprPsqlPass';
```
it is recommended to change it but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Then create database partkeeprpsqldb
```
CREATE DATABASE partkeeprpsqldb OWNER 'partkeeprpsqluser';
```
or if already exist
```
ALTER DATABASE partkeeprpsqldb OWNER TO partkeeprpsqluser;
```
You may change database name but set corresponding environment variable DB_USERNAME and DB_USERPASS
or update PyPnbPartKeepr/settings.

Exit psql client
```
exit
```

### create virtual environment for this application

Generally you need to create an virtual environment except if you have all needed package listed in requirements.txt

#### uv (virtual environment)

Install uv system-wide so the systemd service (running as another user) finds
it in its PATH (`/usr/local/bin` is part of systemd's default PATH):
```bash
curl -LsSf https://astral.sh/uv/install.sh | \
  sudo env UV_INSTALL_DIR=/usr/local/bin INSTALLER_NO_MODIFY_PATH=1 sh
```

uv keeps the virtual environment in `.venv` inside the project, so nothing
has to be exported to place it there.

So in folder of PyPnbPartKeepr, where pyproject.toml is present:
```bash
uv sync --no-dev
```
or for development version (includes dev dependencies)
```bash
uv sync --dev
```

### create table and admin user

copy PyPnbPartKeepr-dist.conf.yaml in PyPnbPartKeepr.conf.yaml or /etc/PyPnbPartKeepr.conf.yaml and update value.
```
cp PyPnbPartKeepr-dist.conf.yaml PyPnbPartKeepr.conf.yaml
```

Update PyBdwsServer.conf.yaml and for SECRET_KEY you may use
```bash
tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50
```

Update database schema
```
uv run ./manage.py migrate
```

Create administrator
```
uv run ./manage.py createsuperuser
```

each time you change static files need to do this:
```
uv run ./manage.py collectstatic
```

### Apache configuration

First in addition to allow reading, you need to allow writing in media folder:
```
setfacl -R -m u:www-data:rwX media
setfacl -R -m d:u:www-data:rwX media
```

#### Mode 1: gunicorn service (recommended)

gunicorn is a runtime dependency, so the `uv sync` above already installed it
in `.venv`; there is nothing more to install here.

create symbolic link of pnbpartkeepr_systemd_venv.service in
/etc/systemd/system/

#### Mode 2: apache mod_wsgi (not the best one)

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
uv run ./manage migrate
```

Create super user

```
uv run ./manage.py createsuperuser
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
sudo service apache2 stop

git pull
git submodule update --init --recursive

uv sync --frozen --no-dev
uv run ./manage.py migrate
uv run ./manage.py collectstatic

sudo systemctl daemon-reload
sudo service apache2 start
```

### Backup

Create a backup, in python environment:

```
uv run --no-sync ./manage.py dbbackup --clean
uv run --no-sync ./manage.py mediabackup --clean
```

To automatise backup put in crontab the line below
```
 27    40      5       *       *       *       /usr/local/pypartkeeper/backup.sh
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
DROP DATABASE partkeeprpsqldb; CREATE DATABASE partkeeprpsqldb OWNER 'partkeeprpsqluser';
SELECT datname,
       pg_encoding_to_char(encoding) AS encoding,
       datcollate,
       datctype
FROM pg_database
ORDER BY datname;
```

Check encoding 'UTF8'

Exit pg client
```
exit
```

Restore a backup, in python environment:

Before check 'BACKUP_DIR' in configuration files
then create a temp directory inside

If database is not setted:
```bash
uv run ./manage.py dbrestore -I [backup_file.psql]
uv run ./manage.py migrate
uv run ./manage.py mediarestore -I [backup_file.tar]
uv run ./manage.py collectstatic
```
if some data not works (too long ... ), edit file and retry... :(

### DevContainer
To use the devcontainer, you need to have Docker installed and the Remote -
Containers extension for Visual Studio Code.

Install Docker: https://docs.docker.com/engine/install/debian/

#### with VScode
Then, open the project in Visual Studio Code and click on the green button in
the bottom left corner to reopen the folder in a container.

#### with command line
install devcontainer-cli:
```
npm install -g @devcontainers/cli
```

Then, you can use the following command to build and run the devcontainer:

```bash
devcontainer up --workspace-folder .
```

#### Start server
Start server in devcontainer with command below and check if you can access to http://localhost:8000

```bash
devcontainer exec --workspace-folder . \
                 uv run ./manage.py runserver 0.0.0.0:8000
```

#### connect to database
```bash
docker exec -it my_devcontainer-db-1 psql -U postgres
```
