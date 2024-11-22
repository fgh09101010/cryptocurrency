from django.db import models

# Create your models here.
# models.py
from django.db import models

class BitcoinPrice(models.Model):
    usd = models.DecimalField(max_digits=15, decimal_places=2)
    eur = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BTC Price at {self.timestamp}"