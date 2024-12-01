from fetch import *
from sql import *


if __name__ == "__main__":
    insert_sql(*fetch_investing())
    insert_sql(*fetch_coindesk()) #先不抓圖片 等內文再一起抓
    insert_sql(*fetch_yahoo())
    for i in no_content():
        insert_content(i[0],fetch_content(i[1],i[2]))
        print(i[0],i[2] ,"資料插入成功")

