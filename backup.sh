#!/bin/sh

cd $(dirname $0)

pipenv run python manage.py dbbackup --clean
pipenv run python manage.py mediabackup --clean
