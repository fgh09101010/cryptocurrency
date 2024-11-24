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

# CoinMarketCap API 金鑰
api_key = '750d435a-83eb-492b-80c4-1698f08650ff'
headers = {
    'X-CMC_PRO_API_KEY': api_key,
    'Accept': 'application/json'
}

# CoinMarketCap API 端點
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
params = {
    'start': '1',  # 從第1名開始
    'limit': '50',  # 取得前 50 種幣
    'convert': 'USD'  # 以 USD 為基準貨幣
}

# 連接到 MariaDB
conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database="cryptocurrency",
    time_zone="+08:00"
)
cursor = conn.cursor()

# 插入數據的 SQL 查詢
insert_query = """
INSERT INTO main_bitcoinprice (coin_id, usd, twd, eur, timestamp)
VALUES (%s, %s, %s, %s, %s)
"""

timestamp = datetime.now() - timedelta(hours=8)  # 當前時間戳

# 獲取幣種列表
response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()['data']
    
    # 獲取美元到歐元的匯率
    conversion_url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
    conversion_params = {
        'amount': 1,  # 換算 1 美元
        'id': 2781,  # USD 的 CoinMarketCap ID
        'convert': 'EUR'
    }
    conversion_response = requests.get(conversion_url, headers=headers, params=conversion_params)
    if conversion_response.status_code == 200:
        eur_conversion_rate = conversion_response.json()['data']['quote']['EUR']['price']

    # 獲取美元到台幣的匯率
    twd_conversion_url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
    twd_conversion_params = {
        'amount': 1,  # 換算 1 美元
        'id': 2781,  # USD 的 CoinMarketCap ID
        'convert': 'TWD'
    }
    twd_conversion_response = requests.get(twd_conversion_url, headers=headers, params=twd_conversion_params)
    if twd_conversion_response.status_code == 200:
        twd_conversion_rate = twd_conversion_response.json()['data']['quote']['TWD']['price']

    # 處理前 50 種幣種
    for coin in data:
        coin_name = coin["name"]  # 幣種名稱 (如 Bitcoin, Ethereum 等)
        coin_abbreviation = coin["symbol"]  # 幣種簡稱 (如 BTC, ETH 等)
        usd_price = float(coin["quote"]["USD"]["price"])  # 美元價格
        eur_price = usd_price * eur_conversion_rate  # 使用實時匯率換算成歐元
        twd_price = usd_price * twd_conversion_rate  # 使用實時匯率換算成台幣

        # 檢查 Coin 資料表是否已經有該幣種
        cursor.execute("SELECT id FROM main_coin WHERE abbreviation = %s", (coin_abbreviation,))
        coin_record = cursor.fetchone()

        # 若 Coin 資料表中沒有該幣種，則插入
        if not coin_record:
            cursor.execute("INSERT INTO main_coin (coinname, abbreviation) VALUES (%s, %s)", (coin_name, coin_abbreviation))
            conn.commit()  # 提交事務
            cursor.execute("SELECT id FROM main_coin WHERE abbreviation = %s", (coin_abbreviation,))
            coin_record = cursor.fetchone()

        # 取得該幣種的 id
        coin_id = coin_record[0]

        # 插入 BitcoinPrice 資料
        cursor.execute(insert_query, (coin_id, usd_price, twd_price, eur_price, timestamp))
        conn.commit()  # 提交事務
        print(f"數據已插入：{coin_name} ({coin_abbreviation}) - USD = {usd_price}, TWD = {twd_price}, EUR = {eur_price}, 時間 = {timestamp}")
else:
    print("請求失敗，狀態碼：", response.status_code)

cursor.close()
conn.close()
