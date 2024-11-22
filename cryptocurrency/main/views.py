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
        response = requests.get(api_url)
        data = response.json()

        usd = data.get('USD')
        eur = data.get('EUR')
        timestamp = datetime.now()  # 使用當前時間作為時間戳

        # 保存價格到資料庫
        BitcoinPrice.objects.create(usd=usd, eur=eur, timestamp=timestamp)

        return JsonResponse({"message": "價格已保存成功！"}, status=200)
    except Exception as e:
        print(f"錯誤: {e}")
        return JsonResponse({"message": "保存價格失敗"}, status=500)

def test_page(request):
    return render(request, 'test.html')

# views.py


