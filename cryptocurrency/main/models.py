from django.db import models

# Create your models here.
# models.py

class BitcoinPrice(models.Model):
    coinname = models.CharField(max_length=50, default="DefaultCoin")
    usd = models.FloatField()
    twd = models.FloatField()
    eur = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BTC Price at {self.timestamp}"