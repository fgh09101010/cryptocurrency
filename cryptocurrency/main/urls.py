from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # 將路徑連結到視圖
    path('crypto/', views.crypto_list, name='crypto_list'),  # 用於展示虛擬貨幣價格的列表頁面（假設已經設置）
    path('crypto/<int:pk>/', views.crypto_detail, name='crypto_detail'),
    path('crypto_change/', views.crypto_change, name='crypto_change'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_profile_image, name='upload_profile_image'),
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_coins, name='favorite_coins'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)