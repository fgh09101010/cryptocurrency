import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

# 時間轉換函數
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
        print("無法解析", time_str)
        return datetime.now().date()

# 抓取內頁圖片函數
def fetch_article_image(article_url):
    # 確保拼接的 URL 是正確的
    if not article_url.startswith("http"):
        full_url = f"https://hk.investing.com{article_url}"  # 拼接完整URL
    else:
        full_url = article_url

    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 定位內頁中的圖片標籤
    img = soup.find('img', class_='h-full w-full object-contain')
    if img and 'src' in img.attrs:
        return img['src']
    return None  # 如果圖片不存在則返回None


# 主函數：抓取新聞
def fetch_investing():
    data = []
    url = "https://hk.investing.com/news/cryptocurrency-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到文章列表
    articles = soup.find_all(class_='list_list__item__dwS6E !mt-0 border-t border-solid border-[#E6E9EB] py-6')

    for article in articles:
        title = article.find('a')
        link = article.find('a')['href']  # 相對路徑
        time = article.find('time')

        # 轉換時間格式
        time = convert_to_datetime(time.text.strip()) if time else datetime.now().date()

        # 抓取內頁圖片
        img_url = fetch_article_image(link)

        # 收集數據
        data.append([title.text.strip(), f"{link}", img_url, time])

    return url, data

# 測試函數
if __name__ == "__main__":
    base_url, articles_data = fetch_investing()
    for article in articles_data:
        print(article)


def fetch_coindesk():
    url="https://www.coindesk.com/"
    return url,[]

def fetch_yahoo():
    url="https://finance.yahoo.com/topic/crypto/"
    return url,[]

