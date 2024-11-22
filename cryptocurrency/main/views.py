from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import BitcoinPrice
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def home(request):
    api_url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR'

    try:
        # 發送請求獲取價格數據
        response = requests.get(api_url)
        data = response.json()

        # 提取價格
        usd = data.get('USD')
        eur = data.get('EUR')
        timestamp = datetime.now()  # 使用當前時間作為時間戳

        # 保存價格到資料庫
        BitcoinPrice.objects.create(usd=usd, eur=eur, timestamp=timestamp)

        # 取得最新的價格資料
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


