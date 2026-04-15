#!/bin/bash
# SPDX-FileCopyrightText: 2025 Pierre-Noel Bouteville  <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

/usr/sbin/service bdws_systemd_venv status
if [ "$?" == "0" ]
then
    echo ""
    echo "*********************************************************************"
    echo "Cannot deploy on running service stop it beffore :"
    echo "    sudo service bdws_systemd_venv stop"
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
echo "    sudo service bdws_systemd_venv start"
