from django.db import models

class Coin(models.Model):
    coinname = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)  # 假設這是加密貨幣的簡稱

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
