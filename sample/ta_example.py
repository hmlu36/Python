import ta
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator
import yfinance as yf
import pandas as pd

# yfinance產出台積電股價資料
stock = yf.Ticker("2330.TW")
df = stock.history(start="2022-01-01", end="2022-12-14")


# 一次性產生40多種技術指標
data = ta.add_all_ta_features(df, "Open", "High", "Low", "Close", "Volume", fillna=True)

# 使用Class ma並且呼叫他的function sma_indicator()
ma = SMAIndicator(df["Close"], 10, fillna=True)
ma = ma.sma_indicator()
print(ma)

# 呼叫布林通道
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)
# 布林中線
bb_bbm = indicator_bb.bollinger_mavg()
# 布林上線pip install --upgrade ta
bb_bbh = indicator_bb.bollinger_hband()
# 布林下線
bb_bbl = indicator_bb.bollinger_lband()
print("布林中線\n", bb_bbm)

# 返回Close是否大於布林上軌，大於的話返回1，反之為0
bb_bbhi = indicator_bb.bollinger_hband_indicator()
# 返回Close是否小於布林下軌，小於的話返回1，反之為0
bb_bbli = indicator_bb.bollinger_lband_indicator()
# 布林帶寬
bb_bbw = indicator_bb.bollinger_wband()
# 布林%b指標 (%b值 = (收盤價−布林帶下軌值) ÷ (布林帶上軌值−布林帶下軌值))
bb_bbp = indicator_bb.bollinger_pband()
