#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py flush --noinput

# 創建超級用戶，設置密碼為 'admin'
python manage.py shell <<EOF
from django.contrib.auth.models import User
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
#python manage.py loaddata ./data.json --no-input