import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re



# 時間轉換函數
def convert_to_datetime(time_str):
    if "年" in time_str and "月" in time_str and "日" in time_str:
        return datetime.strptime(time_str, "%Y年%m月%d日").date()
    elif '小時' in time_str:
        hours_ago = int(re.search(r'(\d+)', time_str).group(0))
        return (datetime.now() - timedelta(hours=hours_ago)).date()
    elif '分钟' in time_str:
        minutes_ago = int(re.search(r'(\d+)', time_str).group(0))
        return (datetime.now() - timedelta(minutes=minutes_ago)).date()
    elif '天' in time_str:
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
    data = []
    url = "https://www.coindesk.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到文章列表
    articles = soup.find_all(class_='bg-white flex gap-6 w-full shrink')

    for article in articles:
        title = article.find('h3').text  # 假設每篇文章的標題都在 <h2> 標籤中
        link = article.find('a', class_="text-color-charcoal-900 mb-4 hover:underline")["href"]

        img_url = ""
        time = article.find('span', class_="Noto_Sans_xs_Sans-400-xs")
        
        if time is None: 
            continue
        
        time_text = time.text.strip()
        
        if "Paid for by" in time_text:
            continue


        if "HRS AGO" in time_text or "MINS AGO" in time_text:

            match = re.match(r"(\d+)\s*(HRS|MINS)\s*AGO", time_text)
            if match:
                number = int(match.group(1))
                unit = match.group(2)
                
                if unit == "HRS":
                    time_obj = datetime.now() - timedelta(hours=number)
                elif unit == "MINS":
                    time_obj = datetime.now() - timedelta(minutes=number)
                    
                time_text = time_obj.strftime("%Y-%m-%d")
        

        else:
            try:
                time_obj = datetime.strptime(time_text, "%b %d, %Y")
                time_text = time_obj.strftime("%Y-%m-%d")
            except ValueError:

                continue
        
        data.append([title, f"https://www.coindesk.com/{link}", img_url, time_text])
    return url,data

def fetch_yahoo():
    url = "https://finance.yahoo.com/topic/crypto/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    current_time = datetime.now()
    articles = soup.find_all('section', class_="container sz-small stream vertical tw-self-start yf-18q3fnf responsive showMobileThumbnails")
    for article in articles:
        # 提取標題（h2 或 h3）
        title_tag = article.find(['h3'], class_=['clamp yf-18q3fnf'])
        title = title_tag.text.strip() if title_tag else "無標題"

        # 提取新聞連結
        link_tag = article.find('a')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else "無連結"

        # 提取圖片連結
        img_tag = article.find('img')
        img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else "無圖片"

        # 提取時間
        time_tag = article.find('div', class_='publishing')
        time_str = time_tag.text.strip() if time_tag else "無時間"

        # 處理時間格式
        time = "無時間"
        if time_str != "無時間":
            # 提取時間描述，如 "12 hours ago"
            if "yesterday" in time_str.lower():
                time = current_time - timedelta(days=1)
            else:
                # 提取時間描述，如 "12 hours ago"
                time_match = re.search(r'(\d+)\s*(hour|minute|second)s?\s*ago', time_str)
                if time_match:
                    number = int(time_match.group(1))
                    unit = time_match.group(2)

                    if unit == "hour":
                        time = current_time - timedelta(hours=number)
                    elif unit == "minute":
                        time = current_time - timedelta(minutes=number)
                    elif unit == "second":
                        time = current_time - timedelta(seconds=number)
                    elif unit == "yesterday":
                        time = current_time - timedelta(days=1)

            # 將時間轉換為 yyyy-mm-dd 格式
            time = time.strftime('%Y-%m-%d')


        # 保存結果
        data.append([title,link if link.startswith('http') else f"https://finance.yahoo.com{link}", img_url, time])
    return url,data

