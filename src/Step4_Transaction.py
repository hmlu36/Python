from fake_useragent import UserAgent
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import Utils
import pandas as pd

'''
url_root = 'https://goodinfo.tw/StockInfo/ShowK_Chart.asp'
payload = {
    'STOCK_ID': '8112',
    'CHT_CAT2': 'DATE',
    'STEP': 'DATA',
    'PERIOD': 365
}

cssSelector = '#divPriceDetail'
df = Utils.PostDataFrameByCssSelector(url_root, payload, cssSelector)
'''

def GetTransactionData(stockId):
    url = f'https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID={stockId}&CHT_CAT2=DATE'
    cssSelector = '#divPriceDetail'
    df = Utils.GetDataFrameByCssSelector(url, cssSelector)
    df.columns = df.columns.get_level_values(1)

    pd.set_option('display.max_rows', df.shape[0]+1)
    #print(df)
    #print(df['收盤'])
    for period in [5, 20, 60]:
        data = pd.to_numeric(df['收盤'], errors='coerce').dropna(how='any',axis=0).head(period)
        #print(data)
        sma = round(data.mean(), 2)
        print(sma)
       
GetTransactionData('1215')