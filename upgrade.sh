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

# uv keeps .venv inside the project by default, so nothing has to be
# exported to place it there. --frozen installs uv.lock as committed and
# fails on a stale lock instead of silently resolving something else.
#
# No gunicorn here: production serves the app through apache mod_wsgi. Add
# `--group gunicorn` if this host runs the systemd service instead.
uv sync --frozen --no-dev
uv run ./manage.py migrate
uv run ./manage.py collectstatic --no-input

echo "You can start service with following command :"
echo "    sudo systemctl daemon-reload"
echo "    sudo service apache2 start"
