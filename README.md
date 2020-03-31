# PyPnbPartKeepr
New Django Version From scratch of PartKeepr
This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for?

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)


## General Setup

### minimal needed package for Debian
```
sudo aptitude install python-pip python-dev python-virtualenv
```

### Create virtual environment for this application

In root of PyPnbPartKeepr:
```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Using MYSQL (not tested imported from older project)


Install client
```
sudo aptitude install libmysqlclient-dev
```

Create user with password and database and give right
  ( note database name end username are always in lower case )

```
CREATE USER PartKeeprAdminUser;
ALTER USER PartKeeprAdminUser WITH ENCRYPTED PASSWORD 'PartKeeprAdminPass';
CREATE DATABASE partkeepradmindb OWNER PartKeeprAdminUser;
```


### PostgreSql Database configuration

Install dependency

```
sudo aptitude install postgresql postgresql-client libpq-dev
```

Add password to postgres user for administration of this

```
sudo passwd postgres
```

Connecting to postgres

```
sudo -i -u postgres
```

Access to postgres:

```
psql
```


### Environment configuration

For easy debug create a file in ~/django_set_env.sh and fill correctly fields:

```
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

* For debug start :
```
./debug_server.sh
```

