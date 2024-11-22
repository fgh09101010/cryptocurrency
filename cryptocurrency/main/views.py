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



# 翻頁
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import BitcoinPrice

def crypto_list(request):
    all_prices = BitcoinPrice.objects.all().order_by('id')  # 獲取所有虛擬貨幣價格

    # 設定每頁顯示的項目數量
    paginator = Paginator(all_prices, 10)  # 每頁顯示10條數據

    # 獲取當前頁面數
    page_number = request.GET.get('page')  # 獲取頁數
    page_obj = paginator.get_page(page_number)  # 根據頁數獲取頁面對象

    return render(request, 'crypto_list.html', {'page_obj': page_obj})






