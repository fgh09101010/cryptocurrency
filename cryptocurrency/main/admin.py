from django.contrib import admin

from .models import Coin,BitcoinPrice
from django.utils.html import format_html

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('coinname', 'abbreviation', 'logo_url',"show_logo")

    def show_logo(self, obj):
        return format_html('<img src="{}" style="height: 40px;"/>', obj.logo_url)


@admin.register(BitcoinPrice)
class BitcoinPriceAdmin(admin.ModelAdmin):
    list_display = ('coin', 'usd', 'twd','eur','timestamp')

    

