import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def convert_to_datetime(time_str):
    if "年" in time_str and "月" in time_str and "日" in time_str:
        return datetime.strptime(time_str, "%Y年%m月%d日").date()
    elif '小時前' in time_str:
        hours_ago = int(re.search(r'(\d+)', time_str).group(0))
        return (datetime.now() - timedelta(hours=hours_ago)).date()
    elif '分鐘前' in time_str:
        minutes_ago = int(re.search(r'(\d+)', time_str).group(0))
        return (datetime.now() - timedelta(minutes=minutes_ago)).date()
    elif '天前' in time_str:
        days_ago = int(re.search(r'(\d+)', time_str).group(0))
        return (datetime.now() - timedelta(days=days_ago)).date()
    else:
        print("無法解析",time_str)
        return (datetime.now()).date() 
    
def fetch_investing():
    data=[]
    url = "https://hk.investing.com/news/cryptocurrency-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all(class_='list_list__item__dwS6E !mt-0 border-t border-solid border-[#E6E9EB] py-6')

    for article in articles:
        title = article.find('a') 
        link = article.find('a')['href']
        img = article.find('img')#抓不到
        time = article.find('time')#1小時前 
        time = convert_to_datetime(time.text.strip())
        data.append([title.text.strip(),link,img,time])
    return url,data

def fetch_coindesk():
    url="https://www.coindesk.com/"
    return url,[]

def fetch_yahoo():
    url="https://finance.yahoo.com/topic/crypto/"
    return url,[]

