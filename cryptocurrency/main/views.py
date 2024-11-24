from django.shortcuts import render, get_object_or_404
import requests
from django.http import JsonResponse
from .models import BitcoinPrice,CryptoData
from datetime import datetime
from django.core.paginator import Paginator

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


# 翻頁
def crypto_list(request):
    query = request.GET.get('query', '') 
    if query:
        all_prices = BitcoinPrice.objects.filter(coin__coinname__icontains=query).order_by('id')
    else:
        all_prices = BitcoinPrice.objects.all().order_by('id')
    

    # 設定每頁顯示的項目數量
    paginator = Paginator(all_prices, 10)  # 每頁顯示10條數據

    # 獲取當前頁面數
    page_number = request.GET.get('page')  # 獲取頁數
    page_obj = paginator.get_page(page_number)  # 根據頁數獲取頁面對象

    return render(request, 'crypto_list.html', {'page_obj': page_obj})


def crypto_detail(request, pk):
    price = get_object_or_404(BitcoinPrice, pk=pk)  # 獲取單一對象，若不存在則返回404
    return render(request, 'crypto_detail.html', {'price': price})

def crypto_change(request):
    change = CryptoData.objects.all()
    return render(request, 'crypto_change.html', {'change': change})

