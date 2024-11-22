import requests
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from pathlib import Path

# 設定 .env 檔案的路徑
env_path = Path(__file__).resolve().parents[2] / '.env'

# 加載 .env 檔案
load_dotenv(dotenv_path=env_path)

# CoinCap API 端點
url = "https://api.coincap.io/v2/assets"

# 發送 GET 請求
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    data = response.json()["data"]  # 解析 JSON 資料，取 "data" 部分
    timestamp = datetime.now() - timedelta(hours=8)  # 調整為 UTC+8

    # 連接到 MariaDB
    conn = mysql.connector.connect(
        host="localhost",  # 替換為你的 MariaDB 主機地址
        user=os.getenv('DB_USER'),  # 替換為你的用戶名
        password=os.getenv('DB_PASSWORD'),  # 替換為你的密碼
        database="cryptocurrency",  # 替換為你的資料庫名稱
        time_zone="+08:00"  # 設定為台灣時間
    )

    cursor = conn.cursor()

    # 插入數據的 SQL 語句
    insert_query = """
    INSERT INTO main_bitcoinprice (coinname, usd, eur, timestamp)
    VALUES (%s, %s, %s, %s)
    """

    # 從 CoinCap API 中提取前 20 種加密貨幣的價格
    for coin in data[:20]:  # 只處理前 20 種幣種
        coin_name = coin["id"]  # 幣種名稱
        usd_price = float(coin["priceUsd"])  # 美元價格
        eur_price = usd_price * 0.94  # 簡單假設匯率換算，實際情況應查詢即時匯率
        cursor.execute(insert_query, (coin_name, usd_price, eur_price, timestamp))

    conn.commit()  # 提交事務
    print(f"數據已插入 {len(data[:20])} 條記錄。")

    cursor.close()
    conn.close()

else:
    print(f"請求失敗，狀態碼: {response.status_code}")
