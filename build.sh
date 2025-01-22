#!/bin/bash

# 更新並安裝系統依賴
apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libpq-dev && apt-get clean

# 安裝 Python 依賴
pip install --no-cache-dir -r requirements.txt

# 執行 Django 遷移命令
python manage.py makemigrations
python manage.py migrate --noinput

# 啟動應用
gunicorn --bind 0.0.0.0:8000 cryptocurrency.wsgi:application
