from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time
from datetime import datetime

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