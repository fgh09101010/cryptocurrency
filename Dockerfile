# 使用官方 Python 映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製需求文件
COPY requirements.txt requirements.txt

# 複製所有應用文件
COPY . .

# 安裝必須的系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libpq-dev && apt-get clean

# 複製 build.sh 腳本
COPY build.sh /app/build.sh

# 賦予腳本執行權限
RUN chmod +x /app/build.sh

# 設定容器啟動時執行 build.sh
CMD ["/app/build.sh"]
