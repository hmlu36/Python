from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import random
import time
import pandas as pd
import os 

def WriteData():    
    cssSelector = '#divStockList'
    sum_df = pd.DataFrame()

    for rankIndex in range(0, 5):
        url = f'https://goodinfo.tw/tw/StockList.asp?SHEET=董監持股&MARKET_CAT=熱門排行&INDUSTRY_CAT=全體董監持股比例&RANK={str(rankIndex)}'
        print(url)

        try:
            time.sleep(random.randint(5, 10))
            df = GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            sum_df = pd.concat([sum_df, df], axis=0)
            #df.columns = df.columns.get_level_values(1)
        except:
            time.sleep(random.randint(20, 30))
            df = GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            #df.columns = df.columns.get_level_values(1)

    # 去除重複標頭
    sum_df[sum_df.ne(sum_df.columns).any(1)].to_csv(f'{GetRootPath()}\Data\Monthly\董監持股比例.csv',encoding='utf_8_sig')


# ------ 共用的 function ------
def GetDataFrameByCssSelector(url, css_selector):
    ua = UserAgent()
    user_agent = ua.random
    headers = {"user-agent": user_agent}
    rawData = requests.get(url, headers=headers)
    rawData.encoding = "utf-8"
    soup = BeautifulSoup(rawData.text, "html.parser")
    data = soup.select_one(css_selector)
    try:
        dfs = pd.read_html(data.prettify())
    except:
        return pd.DataFrame()

    # print(dfs)
    if len(dfs[0]) > 1:
        return dfs[0]
    if len(dfs[1]) > 1:
        return dfs[1]
    return dfs
    
def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------ 測試 ------
'''
WriteData()
'''