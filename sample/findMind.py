# 取得股價
from FinMind.data import DataLoader

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
print(stock_data)