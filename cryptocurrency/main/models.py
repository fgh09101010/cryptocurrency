from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Coin(models.Model):
    coinname = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)  # 假設這是加密貨幣的簡稱
    logo_url = models.URLField(blank=True, null=True)
    api_id = models.BigIntegerField( unique=True, null=True)

    def __str__(self):
        return self.coinname

class BitcoinPrice(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    usd = models.FloatField()
    twd = models.FloatField()
    eur = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.coin.coinname} - {self.timestamp}"
    
class CryptoData(models.Model):
    coin = models.ForeignKey('Coin',on_delete=models.CASCADE,related_name='crypto_data',)  
    price_usd = models.DecimalField(max_digits=20, decimal_places=2)  # 美金價格
    price_twd = models.DecimalField(max_digits=20, decimal_places=2)  # 新台幣價格
    price_eur = models.DecimalField(max_digits=20, decimal_places=2)  # 歐元價格
    market_cap = models.DecimalField(max_digits=30, decimal_places=2)  # 市值
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2)  # 24小時交易量
    change_24h = models.DecimalField(max_digits=5, decimal_places=2)  # 24小時變動百分比
    fetched_at = models.DateTimeField()  # 資料抓取時間

    def __str__(self):
        return f"{self.coin.coinname}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', null=True)
    favorite_coin = models.ManyToManyField(Coin, blank=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class NewsWebsite(models.Model):
    name = models.CharField(max_length=255, unique=True)  # 新聞網站名稱

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)  # 標題
    url = models.URLField(max_length=255)  # 網址
    image_url = models.URLField(null=True,max_length=500)  # 圖片網址
    content = models.TextField(null=True)  # 內文欄位，使用 TextField 儲存長篇文字內容
    time = models.DateTimeField()
    website = models.ForeignKey(NewsWebsite, on_delete=models.CASCADE)  # 外鍵關聯到新聞網站

    def __str__(self):
        return self.title
    
    
class CoinHistory(models.Model):
    coin = models.ForeignKey(Coin, related_name='history', on_delete=models.CASCADE)  # 外鍵，關聯到 Coin 模型
    date = models.DateTimeField()  # 日期
    open_price = models.DecimalField(max_digits=20, decimal_places=2)  # 開盤價
    high_price = models.DecimalField(max_digits=20, decimal_places=2)  # 最高價
    low_price = models.DecimalField(max_digits=20, decimal_places=2)  # 最低價
    close_price = models.DecimalField(max_digits=20, decimal_places=2)  # 收盤價
    volume = models.DecimalField(max_digits=20, decimal_places=2)  # 成交量

    def __str__(self):
        return f"{self.coin.name} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    

class XPost(models.Model):
    ids = models.CharField(max_length=255, unique=True)
    html = models.TextField()
    text = models.TextField()

    def __str__(self):
        return f"Tweet ID: {self.ids}"