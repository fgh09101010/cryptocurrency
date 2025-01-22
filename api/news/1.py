from fetch import *
from sql import *

#預計一天一次
if __name__ == "__main__":
    insert_sql(*fetch_investing())
    insert_sql(*fetch_coindesk())
    insert_sql(*fetch_yahoo())
    for i in no_content():
        insert_content(i[0],fetch_content(i[1],i[2]))
        print(i[0],i[2] ,"資料插入成功")

    insert_image_url("https://hk.investing.com/news/cryptocurrency-news", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcrwkwizaO4rpZ8b4af74qxlZKh6YK98JjGw&s")
    insert_image_url("https://www.coindesk.com/", "https://logos-world.net/wp-content/uploads/2023/02/CoinDesk-Logo.png")
    insert_image_url("https://finance.yahoo.com/topic/crypto/", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Yahoo%21_Finance_logo_2021.png/1200px-Yahoo%21_Finance_logo_2021.png")

