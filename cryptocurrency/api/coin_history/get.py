import ccxt
from datetime import datetime


def get_history(coin):
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # 設定交易對和時間間隔
    symbol = f'{coin}/USDT'  # 交易對
    timeframe = '1d'     # K 線圖的時間間隔，例如 '1m', '5m', '1h', '1d'
    since = exchange.parse8601('2024-11-01T00:00:00Z')  # 開始時間

    # 獲取歷史數據
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    data=[]
    # 轉換數據為易讀格式
    for entry in ohlcv:
        timestamp, open_, high, low, close, volume = entry
        date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        data.append([date,open_,high,low,close,volume])
    return data