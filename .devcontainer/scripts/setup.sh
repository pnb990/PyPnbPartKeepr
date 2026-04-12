#!/bin/sh -e

set -x

echo "Setting up the development environment..."

echo "Creating PostgreSQL database and user..."
.devcontainer/scripts/create_db.sh

echo "Setting up Python virtual environment with Pipenv..."
pipenv sync --dev

echo "Copying configuration files..."
if [ ! -f PyPnbPartKeepr.conf.yaml ]; then
    echo "Copying PyPnbPartKeepr-dist.conf.yaml to PyPnbPartKeepr.conf.yaml"
    cp PyPnbPartKeepr-dist.conf.yaml PyPnbPartKeepr.conf.yaml
    # Override DB_HOST for devcontainer
    python3 -c "
import yaml
with open('PyPnbPartKeepr.conf.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['DB_HOST'] = 'db'
cfg['DEBUG'] = True
cfg['ALLOWED_HOSTS'] = ['*']
with open('PyPnbPartKeepr.conf.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False)
"
else
    echo "PyPnbPartKeepr.conf.yaml already exists, skipping copy."
fi

echo "Running database migrations..."
pipenv run python3 ./manage.py migrate

echo "Creating superuser account..."
cat <<EOF | pipenv run python3 ./manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
EOF

echo "Setting up media and static directories..."
sudo mkdir -p ${MEDIA_ROOT:-/var/partkeepr/media}
sudo setfacl -R -m u:${USER}:rwX ${MEDIA_ROOT:-/var/partkeepr/media}
sudo setfacl -R -m d:u:${USER}:rwX ${MEDIA_ROOT:-/var/partkeepr/media}

sudo mkdir -p ${STATIC_ROOT:-/var/partkeepr/static}
sudo setfacl -R -m u:${USER}:rwX ${STATIC_ROOT:-/var/partkeepr/static}
sudo setfacl -R -m d:u:${USER}:rwX ${STATIC_ROOT:-/var/partkeepr/static}

sudo mkdir -p ${BACKUP_DIR:-/var/partkeepr/backups}
sudo setfacl -R -m u:${USER}:rwX ${BACKUP_DIR:-/var/partkeepr/backups}
sudo setfacl -R -m d:u:${USER}:rwX ${BACKUP_DIR:-/var/partkeepr/backups}

echo "Collecting static files..."
pipenv run python3 ./manage.py collectstatic --noinput

echo "Development environment setup complete."
