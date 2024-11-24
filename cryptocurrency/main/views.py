from django.shortcuts import render, get_object_or_404,redirect
import requests
from django.http import JsonResponse
from .models import BitcoinPrice,CryptoData,UserProfile,Coin
from datetime import datetime
from django.core.paginator import Paginator
# 登入頁面
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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



def crypto_detail(request, pk):
    price = get_object_or_404(BitcoinPrice, pk=pk)  # 獲取單一對象，若不存在則返回404
    return render(request, 'crypto_detail.html', {'price': price})

def crypto_change(request):
    change = CryptoData.objects.all()
    return render(request, 'crypto_change.html', {'change': change})


# 登入頁面
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 登入成功後跳轉到首頁
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# 登出功能
def logout_view(request):
    logout(request)
    return redirect('home')  # 登出後跳轉到登入頁

# 需要登入的頁面保護
# @login_required
# def crypto_list(request):
#     query = request.GET.get('query', '') 
#     if query:
#         all_prices = BitcoinPrice.objects.filter(coin__coinname__icontains=query).order_by('id')
#     else:
#         all_prices = BitcoinPrice.objects.all().order_by('id')
    
#     paginator = Paginator(all_prices, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'crypto_list.html', {'page_obj': page_obj})


from django.db.models import F
from django.core.paginator import Paginator
from django.shortcuts import render

def crypto_list(request):
    query = request.GET.get('query', '') 
    sort_by = request.GET.get('sort_by')  # 排序欄位
    sort_order = request.GET.get('sort_order')  # 排序狀態（"asc", "desc", "default"）

    if query:
        all_prices = BitcoinPrice.objects.filter(coin__coinname__icontains=query)
    else:
        all_prices = BitcoinPrice.objects.all()

    # 根據排序狀態進行排序
    if sort_by and sort_order == 'asc':
        all_prices = all_prices.order_by(sort_by)  # A-Z 排序
    elif sort_by and sort_order == 'desc':
        all_prices = all_prices.order_by(F(sort_by).desc())  # Z-A 排序
    # "default" 狀態下不進行排序，保持自然順序

    paginator = Paginator(all_prices, 10)  # 每頁顯示10條數據
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'crypto_list.html', {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'sort_order': sort_order,
    })


from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # 或跳轉到其他頁面
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'upload.html', {'form': form})

@login_required
def add_to_favorites(request, pk):
    user_profile = request.user.profile
    try:
        # 根據 pk 查詢 Coin 物件
        crypto = Coin.objects.get(id=pk)
        print(crypto)
        # 將該 Coin 添加到 user's favorite_cryptos
        user_profile.favorite_coin.add(crypto)
        user_profile.save()
    except Coin.DoesNotExist:
        print(f"Coin with ID {pk} not found")  # 如果沒有找到 Coin，打印信息
    except Exception as e:
        print(f"An error occurred: {e}")  # 其他異常處理
    return redirect('crypto_list')  # 重定向回顯示幣列表的頁面

@login_required
def favorite_coins(request):
    user_profile = request.user.profile
    favorite_cryptos = user_profile.favorite_coin.all()  # 獲取用戶的最愛幣
    return render(request, 'favorite_coins.html', {'favorite_cryptos': favorite_cryptos})