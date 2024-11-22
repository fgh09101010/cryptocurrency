# import mysql.connector
# import os

# try:
#     conn = mysql.connector.connect(
#         host="localhost",  # 替換為你的 MariaDB 主機地址
#         user="root",  # 替換為你的用戶名
#         password="root",  # 替換為你的密碼
#         database="cryptocurrency"  # 替換為你的資料庫名稱
#     )

#     # 如果連接成功，會進入這個區塊
#     if conn.is_connected():
#         print("資料庫連接成功！")
#     else:
#         print("資料庫連接失敗！")

# except mysql.connector.Error as err:
#     print(f"資料庫連接出錯: {err}")
# finally:
#     if conn.is_connected():
#         conn.close()  # 關閉資料庫連接
