from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import BitcoinPrice
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def home(request):
    from django.shortcuts import render
from .models import BitcoinPrice
import requests
from datetime import datetime

def home(request):
    try:
        # 取得資料庫中的最新價格
        latest_price = BitcoinPrice.objects.last()

        # 如果資料庫中沒有資料，從 API 獲取並保存價格
        if not latest_price:
            api_url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR'
            response = requests.get(api_url)
            data = response.json()

            # 提取價格
            usd = data.get('USD')
            eur = data.get('EUR')
            timestamp = datetime.now()  # 使用當前時間作為時間戳

            # 保存價格到資料庫
            BitcoinPrice.objects.create(usd=usd, eur=eur, timestamp=timestamp)

            # 重新取得最新價格
            latest_price = BitcoinPrice.objects.last()

        # 渲染到模板
        return render(request, 'home.html', {
            'usd': latest_price.usd,
            'eur': latest_price.eur,
            'timestamp': latest_price.timestamp,
        })
    except Exception as e:
        print(f"錯誤: {e}")
        return render(request, 'home.html', {
            'error': '無法獲取價格，請稍後再試。'
        })


def test_page(request):
    return render(request, 'test.html')

# views.py


