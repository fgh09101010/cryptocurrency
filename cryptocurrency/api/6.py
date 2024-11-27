import ccxt
from datetime import datetime
import mysql.connector

# 初始化交易所
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# 設定交易對和時間間隔
symbol = 'BTC/USDT'  # 交易對
timeframe = '1d'     # K 線圖的時間間隔，例如 '1m', '5m', '1h', '1d'
since = exchange.parse8601('2024-11-01T00:00:00Z')  # 開始時間

# 獲取歷史數據
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)

# 轉換數據為易讀格式
print("日期, 開盤價, 最高價, 最低價, 收盤價, 成交量")
for entry in ohlcv:
    timestamp, open_, high, low, close, volume = entry
    date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{date}, {open_}, {high}, {low}, {close}, {volume}")