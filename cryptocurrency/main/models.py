from django.db import models

class Coin(models.Model):
    coinname = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)  # 假設這是加密貨幣的簡稱
    logo_url = models.URLField(blank=True, null=True)

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
    coin_name = models.CharField(max_length=100)  # 幣種名稱
    price_usd = models.DecimalField(max_digits=20, decimal_places=2)  # 美金價格
    price_twd = models.DecimalField(max_digits=20, decimal_places=2)  # 新台幣價格
    price_eur = models.DecimalField(max_digits=20, decimal_places=2)  # 歐元價格
    market_cap = models.DecimalField(max_digits=30, decimal_places=2)  # 市值
    volume_24h = models.DecimalField(max_digits=30, decimal_places=2)  # 24小時交易量
    change_24h = models.DecimalField(max_digits=5, decimal_places=2)  # 24小時變動百分比
    fetched_at = models.DateTimeField()  # 資料抓取時間

    def __str__(self):
        return self.coin_name
    
