from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time


def GetDistribution(stockId):
    url = f'https://goodinfo.tw/tw/EquityDistributionClassHis.asp?STOCK_ID={stockId}'
    cssSelector = '#divDetail'
    try:
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(1)
    except:
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(1)
    
    # 千張大戶
    data = pd.to_numeric(df['＞1千張'], errors='coerce').dropna(how='any',axis=0).head(3)
    return ' / '.join(map(str, list(data)))


data = GetDistribution('1515')
print(data)
