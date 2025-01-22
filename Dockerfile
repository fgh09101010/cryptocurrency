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

# 執行 Django 遷移命令
RUN python manage.py makemigrations
RUN python manage.py migrate --noinput

# 暴露應用端口
EXPOSE 8000

# 啟動應用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cryptocurrency.wsgi:application"]
