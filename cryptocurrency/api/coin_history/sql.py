import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime
env_path = Path(__file__).resolve().parents[2] / '.env'

# 加載 .env 檔案
load_dotenv(dotenv_path=env_path)

def get_name():
    # 設定 .env 檔案的路徑

    # 初始化交易所
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database="cryptocurrency",
        time_zone="+08:00"
    )

    # 創建cursor物件
    cursor = conn.cursor()

    # 編寫查詢語句，抓取十筆abbreviation
    query = "SELECT id, abbreviation FROM main_coin LIMIT 10;"

    # 執行查詢
    cursor.execute(query)

    # 獲取結果
    abbreviations = cursor.fetchall()
    # 關閉連接
    cursor.close()
    conn.close()
    return abbreviations

def save_data(coin_id,data):
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database="cryptocurrency",
        time_zone="+08:00"
    )

    # 創建cursor物件
    cursor = conn.cursor()

    # 資料

    # 將字符串日期轉換為 DATETIME
    date = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S')

    # 編寫插入語句
    query = """
    INSERT INTO main_coinhistory (date, open_price, high_price, low_price, close_price, volume, coin_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    # 執行插入
    cursor.execute(query, (date, data[1], data[2], data[3], data[4], data[5], coin_id))

    # 提交事務
    conn.commit()

    # 顯示插入的資料
    print(f"資料已插入：{date}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {coin_id}")

    # 關閉連接
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print(get_name())