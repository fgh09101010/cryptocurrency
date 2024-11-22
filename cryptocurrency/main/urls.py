from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 將路徑連結到視圖
    path('test/', views.test_page, name='test_page'),
]