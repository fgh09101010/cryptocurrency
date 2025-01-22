# 使用官方 Python 映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libpq-dev && apt-get clean

# 複製文件
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有應用文件
COPY . .

# 下載 wait-for-it 腳本
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# 在容器啟動時等待 PostgreSQL 服務啟動
CMD wait-for-it db:5432 -- python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8000 cryptocurrency.wsgi:application
