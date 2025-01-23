from celery import shared_task
from datetime import datetime, timedelta
import os
from .crawler.news import *
from data_collector.coin_history.ccxt_price import CryptoHistoryFetcher
from data_collector.new_scraper import site_all

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptocurrency.settings')
@shared_task
def news_crawler():
    from .models import NewsWebsite,NewsArticle
    from django.db.models import Q

    websites=site_all.website()
    for site in websites:
        NewsWebsite.objects.update_or_create(
                url=site.url,
                defaults={
                "name":site.name,
                'icon_url': site.icon_url,
            },
            )
        website_instance = NewsWebsite.objects.get(name=site.name)
        
        for article in site.fetch_page():
            defaults = {
            'title': article["title"],
            'time': article["time"],
            'website': website_instance
            }

            # 如果 image_url 存在，加入到 defaults
            if article.get("image_url"):
                defaults['image_url'] = article["image_url"]

            NewsArticle.objects.update_or_create(
                url=article["url"],
                defaults=defaults,
            )

    articles_empty = NewsArticle.objects.filter(
        Q(content__isnull=True) | Q(content__exact="") | Q(image_url__isnull=True) | Q(image_url__exact="")
    )
    for article in articles_empty:
        try :
            a=site_all.article(article)
            if a:
                
                    a.get_news_details()
                    NewsArticle.objects.update_or_create(
                            url=a.url,
                            defaults={
                            'title': a.title,
                            'time': a.time,
                            'image_url':a.image_url,
                            "content":a.content,
                            'website':a.website
                        },
                        )
                    print(a.title)
        except:
            continue





@shared_task
def fetch_history():
    from django.db.models import Max
    from .models import Coin,CoinHistory

    coin_history = Coin.objects.all().order_by('id')[:10]
    result = []
    for coin in coin_history:
        # 查找該 coin 的最新日期
        latest_history = CoinHistory.objects.filter(coin=coin).aggregate(latest_date=Max('date'))
        latest_date = latest_history['latest_date']

        # 若找不到最新日期，設定為 2025-01-01
        if latest_date is None:
            latest_date = datetime(2025, 1, 1, 0, 0)
        else:
            latest_date = latest_date + timedelta(minutes=1)
        result.append((coin, latest_date))
    for i in result:
        c=CryptoHistoryFetcher(i[0].abbreviation,i[1])
        coin = Coin.objects.get(abbreviation=c.coin,api_id=i[0].api_id)
        data=c.get_history()
        for history_data in data:
            date = datetime.strptime(history_data[0], '%Y-%m-%d %H:%M:%S')
            date=str(date)+"+00:00"
            open_price = history_data[1]
            high_price = history_data[2]
            low_price = history_data[3]
            close_price = history_data[4]
            volume = history_data[5]
            
            # 儲存歷史資料進入資料庫
            CoinHistory.objects.create(
                coin=coin,
                date=date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume,
            )
        print(f"存入資料庫{len(data)}筆：{c.coin} {history_data[0]}")


def test():
    from decimal import Decimal
    from .models import Coin,CoinHistory,NewsWebsite,NewsArticle,BitcoinPrice
    website, created = NewsWebsite.objects.get_or_create(
    url="https://hk.investing.com/news/cryptocurrency-news",
    defaults={
        'name': "investing",
        'icon_url': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcrwkwizaO4rpZ8b4af74qxlZKh6YK98JjGw&s"
    }
)

    # 使用 get_or_create() 檢查並新增 NewsArticle 資料
    article, created = NewsArticle.objects.get_or_create(
        url="https://hk.investing.com/news/cryptocurrency-news/article-93CH-724501",
        defaults={
            'title': "以太坊交易收入選後飆升 - 報告",
            'image_url': "https://i-invdn-com.investing.com/news/LYNXNPED840XB_L.jpg",
            'content': "這是一段範例新聞的內文內容。",
            'time': datetime.now(),
            'website': website
        }
    )

    # 使用 get_or_create() 檢查並新增 Coin 資料
    coin, created = Coin.objects.get_or_create(
        abbreviation="BTC",
        defaults={
            'coinname': "Bitcoin",
            'logo_url': "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
            'api_id': 1
        }
    )

    # 使用 get_or_create() 檢查並新增 CoinHistory 資料
    coin_history, created = CoinHistory.objects.get_or_create(
        coin=coin,
        defaults={
            'date' :datetime.now(),
            'open_price': Decimal("21000.1234567890"),
            'high_price': Decimal("21500.1234567890"),
            'low_price': Decimal("20800.1234567890"),
            'close_price': Decimal("21200.1234567890"),
            'volume': Decimal("50000.1234567890")
        }
    )

    # 使用 get_or_create() 檢查並新增 BitcoinPrice 資料
    bitcoin_price, created = BitcoinPrice.objects.get_or_create(
        coin=coin,
        defaults={
            'timestamp' : datetime.now(),
            'usd': 21200.12,
            'twd': 659000.56,
            'jpy': 2890000.45,
            'eur': 19800.67,
            'market_cap': Decimal("400000000000.00"),
            'volume_24h': Decimal("20000000000.00"),
            'change_24h': Decimal("-1.23")
        }
    )
    print("成功")
'''
from main.task import fetch_history,news_crawler,test
fetch_history()
news_crawler()
test()
'''