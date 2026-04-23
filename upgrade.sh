#!/bin/bash
# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville  <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

/usr/sbin/service apache2 status
if [ "$?" == "0" ]
then
    echo ""
    echo "*********************************************************************"
    echo "Cannot deploy on running service stop it beffore :"
    echo "    sudo service apache2 stop"
    echo "*********************************************************************"
    exit 1
fi

git pull
git submodule update --init --recursive

export PIPENV_VENV_IN_PROJECT=1
pipenv install --deploy
pipenv run ./manage.py migrate
pipenv run ./manage.py collectstatic --no-input

echo "You can start service with following command :"
echo "    sudo systemctl daemon-reload"
echo "    sudo service apache2 start"
