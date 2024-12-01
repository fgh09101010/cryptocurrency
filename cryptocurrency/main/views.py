from django.shortcuts import render, get_object_or_404,redirect
import requests
from django.http import JsonResponse,HttpResponseRedirect
from .models import BitcoinPrice,UserProfile,Coin,NewsWebsite,NewsArticle,CoinHistory,XPost
from datetime import datetime
from django.core.paginator import Paginator
# 登入頁面
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import plotly.graph_objects as go
 
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
    # 查詢 CoinHistory 資料
    coin_history = CoinHistory.objects.filter(coin_id=pk).order_by('date')

    # 準備資料
    dates = [entry.date for entry in coin_history]
    open_prices = [entry.open_price for entry in coin_history]
    high_prices = [entry.high_price for entry in coin_history]
    low_prices = [entry.low_price for entry in coin_history]
    close_prices = [entry.close_price for entry in coin_history]

    # 創建 K 線圖
    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
        name="Candlestick"
    )])

    # 更新圖表的布局
    fig.update_layout(
        title=f"Price History for Coin {pk}",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    # 將圖表的 HTML 代碼傳遞到模板
    graph = fig.to_html(full_html=False)
    price = get_object_or_404(BitcoinPrice, pk=pk)  # 獲取單一對象，若不存在則返回404
    return render(request, 'crypto_detail.html', {'price':price,'graph': graph})
    


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
    if request.user.is_authenticated:
        user_profile = request.user.profile
        favorite_coin_ids = list(user_profile.favorite_coin.values_list('id', flat=True))
    else:
        favorite_coin_ids = []
    
    return render(request, 'crypto_list.html', {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'favorite_coin_ids': favorite_coin_ids,
    })


from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # 取得上傳的圖片
            image = request.FILES.get('profile_image')

            # 如果有圖片上傳，進行處理
            if image:
                # 使用 Pillow 處理圖片
                img = Image.open(image)

                # 將圖片轉換為 RGB 格式，並保存為 JPG
                img = img.convert('RGB')

                # 設定最大寬度與高度（可根據需要調整）
                max_width = 500
                max_height = 500
                img.thumbnail((max_width, max_height))

                # 保存為 JPG 格式
                image_io = BytesIO()
                img.save(image_io, format='JPEG')
                image_io.seek(0)

                # 將處理過的圖片轉為 Django 可以儲存的 ContentFile
                image_name = f"{image.name.split('.')[0]}.jpg"  # 保留原檔名，但轉為 .jpg
                user_profile_image = ContentFile(image_io.read(), name=image_name)

                # 更新用戶檔案中的圖片
                request.user.profile.profile_image.save(image_name, user_profile_image)

            # 提交表單後，跳轉到主頁
            return redirect('home')  # 或者你可以跳轉到其他頁面
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
def remove_from_favorites(request, pk):
    user_profile = request.user.profile
    try:
        # 根據 pk 查詢 Coin 物件
        crypto = Coin.objects.get(id=pk)
        print(crypto)
        # 從 user's favorite_cryptos 刪除該 Coin
        user_profile.favorite_coin.remove(crypto)
        user_profile.save()
        print(f"Removed {crypto.coinname} from favorites")  # 提示刪除成功
    except Coin.DoesNotExist:
        print(f"Coin with ID {pk} not found")  # 如果沒有找到 Coin，打印信息
    except Exception as e:
        print(f"An error occurred: {e}")  # 其他異常處理
    referer = request.META.get('HTTP_REFERER', '/')  # 默認重定向到根目錄
    return HttpResponseRedirect(referer)

@login_required
def favorite_coins(request):
    user_profile = request.user.profile
    favorite_cryptos = user_profile.favorite_coin.all()  # 獲取用戶的最愛幣
    return render(request, 'favorite_coins.html', {'favorite_cryptos': favorite_cryptos})

def news_list(request):  
    # 讀取所有新聞文章，並根據時間排序
    all_articles = NewsArticle.objects.all().order_by('-time')  # 按時間欄位倒序排序
    return render(request, 'news_list.html', {'all_articles': all_articles})


def coin_history(request, coin_id):
    # 查詢 CoinHistory 資料
    coin_history = CoinHistory.objects.filter(coin_id=coin_id).order_by('date')

    # 準備資料
    dates = [entry.date for entry in coin_history]
    open_prices = [entry.open_price for entry in coin_history]
    high_prices = [entry.high_price for entry in coin_history]
    low_prices = [entry.low_price for entry in coin_history]
    close_prices = [entry.close_price for entry in coin_history]

    # 創建 K 線圖
    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
        name="Candlestick"
    )])

    # 更新圖表的布局
    fig.update_layout(
        title=f"Price History for Coin {coin_id}",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )

    # 將圖表的 HTML 代碼傳遞到模板
    graph = fig.to_html(full_html=False)

    return render(request, 'coin_history.html', {'graph': graph})


def X_list(request):
    # 获取指定 id 的 XPost 对象
    xposts = XPost.objects.all()
    return render(request, 'x_list.html', {'xposts': xposts})