#!/bin/sh

# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

cd $(dirname $0)

# --no-sync: this runs unattended from cron, so it must use .venv as the
# deploy left it rather than re-resolving and mutating it behind the
# service's back. See pnbpartkeepr_systemd_venv.service.
uv run --no-sync python manage.py dbbackup --clean
uv run --no-sync python manage.py mediabackup --clean
