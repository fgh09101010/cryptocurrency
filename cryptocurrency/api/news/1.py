from fetch import *
from sql import insert_sql


if __name__ == "__main__":
    insert_sql(*fetch_investing())
    insert_sql(*fetch_coindesk()) #先不抓圖片 等內文再一起抓
    insert_sql(*fetch_yahoo())
