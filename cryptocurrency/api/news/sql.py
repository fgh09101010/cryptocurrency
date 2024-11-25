import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path

# 設定 .env 檔案的路徑
env_path = Path(__file__).resolve().parents[3] / '.env'

# 加載 .env 檔案
load_dotenv(dotenv_path=env_path)

def insert_sql(website_name, articles):
    # 資料庫連接配置
    conn = mysql.connector.connect(
        host="localhost",  # 替換為你的資料庫主機地址
        user=os.getenv('DB_USER'),  # 替換為你的用戶名
        password=os.getenv('DB_PASSWORD'),  # 替換為你的密碼
        database="cryptocurrency",  # 替換為你的資料庫名稱
        time_zone="+08:00"  # 設定為台灣時間
    )

    cursor = conn.cursor()

    # 檢查網站是否存在
    select_website_query = "SELECT id FROM `main_newswebsite` WHERE `name` = %s"
    cursor.execute(select_website_query, (website_name,))
    website_id = cursor.fetchone()

    # 如果找不到對應的網站資料，則插入新網站
    if website_id is None:
        insert_website_query = "INSERT INTO `main_newswebsite` (`name`) VALUES (%s)"
        cursor.execute(insert_website_query, (website_name,))
        conn.commit()  # 確保資料插入後獲取新 ID
        website_id = cursor.lastrowid  # 獲取新增記錄的 ID
    else:
        website_id = website_id[0]  # 提取 website_id

    # 插入文章資料
    insert_article_query = """
    INSERT INTO `main_newsarticle` (`title`, `url`, `image_url`, `time`, `website_id`)
    VALUES (%s, %s, %s, %s, %s)
    """

    # 插入每篇文章資料
    for article in articles:
        cursor.execute(insert_article_query, (article[0], article[1], article[2], article[3], website_id))

    # 提交變更
    conn.commit()

    # 關閉遊標和連接
    cursor.close()
    conn.close()

    print(f"{website_name}資料成功插入！")
