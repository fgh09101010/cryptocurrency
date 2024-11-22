from django.shortcuts import render
import requests
from django.http import JsonResponse
from .models import BitcoinPrice
from datetime import datetime

# Create your views here.

from django.shortcuts import render
from .models import BitcoinPrice

def home(request):
    try:
        # 取得資料庫中的所有價格，按 id 升序排列
        all_prices = BitcoinPrice.objects.all().order_by('id')

        # 渲染到模板
        return render(request, 'home.html', {
            'all_prices': all_prices,
        })

    except Exception as e:
        print(f"錯誤: {e}")
        return render(request, 'home.html', {
            'error': '無法獲取資料，請稍後再試。'
        })



def test_page(request):
    return render(request, 'test.html')



