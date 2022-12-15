# 取得股價
from FinMind.data import DataLoader
import requests
import pandas as pd
import os

dl = DataLoader()
# 下載台股股價資料
stock_data = dl.taiwan_stock_daily(
    stock_id='2330', start_date='2022-01-01', end_date='2022-12-13'
)
# 下載三大法人資料
stock_data = dl.feature.add_kline_institutional_investors(
    stock_data
) 
# 下載融資券資料
stock_data = dl.feature.add_kline_margin_purchase_short_sale(
    stock_data
)
#print(stock_data)


# stock_data.to_csv(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\Data\FinMind.csv", encoding="utf_8_sig")

# 股票綜合損益表
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockFinancialStatements",
    "data_id": "2330",
    "start_date": "2022-06-01",
    "end_date": "2022-12-01"  # 不加則抓到現在日期
}
r = requests.get(url, params=parameter)
data = r.json()
stock_income_statement = data["data"]
#print(pd.DataFrame(stock_income_statement))


# 股利政策表 
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockDividend",
    "data_id": "00692",
    "start_date": "2021-01-01"
}

r = requests.get(url, params=parameter)
data = r.json()
stock_dividend = data["data"]
stock_data = pd.DataFrame(stock_dividend)
stock_data.to_csv(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\Data\股利政策表.csv", encoding="utf_8_sig")
