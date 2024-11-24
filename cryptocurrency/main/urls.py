from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 將路徑連結到視圖
    path('crypto/', views.crypto_list, name='crypto_list'),  # 用於展示虛擬貨幣價格的列表頁面（假設已經設置）
    path('crypto/<int:pk>/', views.crypto_detail, name='crypto_detail'),
<<<<<<< HEAD
    path('crypto_change/', views.crypto_change, name='crypto_change'),
=======
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
>>>>>>> cdd587bd17d0e71f60cb27bc8813af7554292b9c
]
