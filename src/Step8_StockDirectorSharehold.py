from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time
from datetime import datetime

# https://github.com/rifleak74/MarketDataScience/blob/master/%E7%A8%8B%E5%BC%8F%E9%87%91%E8%9E%8D%E9%A1%9E/%E5%86%A0%E8%BB%8D%E9%81%B8%E8%82%A1%E7%AD%96%E7%95%A5/choose_stock1.py

def GetDirectorSharehold(stockId):
    url = f'https://goodinfo.tw/tw/StockDirectorSharehold.asp?STOCK_ID={stockId}'
    cssSelector = '#divDetail'
    try:
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        print(df)
        #df.columns = df.columns.get_level_values(3)
    except:
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        #df.columns = df.columns.get_level_values(3)

    
GetDirectorSharehold('2330')