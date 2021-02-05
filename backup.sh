#!/bin/sh

cd $(dirname $0)

../venv/bin/python manage.py dbbackup --clean
../venv/bin/python manage.py mediabackup --clean
