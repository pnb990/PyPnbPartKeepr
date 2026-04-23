#!/bin/sh

# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

cd $(dirname $0)

pipenv run python manage.py dbbackup --clean
pipenv run python manage.py mediabackup --clean
