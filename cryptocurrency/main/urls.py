from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 將路徑連結到視圖
    path('test/', views.test_page, name='test_page'),
    path('crypto/', views.crypto_list, name='crypto_list'),  # 用於展示虛擬貨幣價格的列表頁面（假設已經設置）

]