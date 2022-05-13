from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time
import os

def WriteData():    
    cssSelector = '#divStockList'
    sum_df = pd.DataFrame()

    for rankIndex in range(0, 5):
        url = f'https://goodinfo.tw/tw/StockList.asp?SHEET=董監持股&MARKET_CAT=熱門排行&INDUSTRY_CAT=全體董監持股比例&RANK={str(rankIndex)}'
        print(url)

        try:
            time.sleep(random.randint(5, 10))
            df = Utils.GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            sum_df = pd.concat([sum_df, df], axis=0)
            #df.columns = df.columns.get_level_values(1)
        except:
            time.sleep(random.randint(20, 30))
            df = Utils.GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            #df.columns = df.columns.get_level_values(1)

    # 去除重複標頭
    sum_df[sum_df.ne(sum_df.columns).any(1)].to_csv(f'{Utils.GetRootPath()}\Data\Monthly\董監持股比例.csv',encoding='utf_8_sig')

'''
GetDirectorSharehold()
'''