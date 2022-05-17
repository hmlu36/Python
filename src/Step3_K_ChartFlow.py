import pandas as pd
import src.Utils as Utils
import re
from src.BrowserUserAgent import GetHeader
import requests
from bs4 import BeautifulSoup
import random
import time
'''
抓取本益比
取得現今EPS、本益比、近五年六個級距本益比

選股條件：
1. 本益比小於10
2. 小於近五年最小級距本益比
'''
def GetPE(stockId):
    url = f'https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stockId}&CHT_CAT=WEEK'
    css_selector = '#divK_ChartFlowDetail'
    try:
        df = Utils.GetDataFrameByCssSelector(url, css_selector)
        # 取前兩列後面倒數6欄資料
        firtRowDf = df.iloc[0,-6:]
        #print(firtRowDf)
    except:
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, css_selector)
        
        # 取前兩列後面倒數6欄資料
        firtRowDf = df.iloc[0,-6:]
        #print(firtRowDf)
    
    #dataframe轉成dictionary 參考 https://stackoverflow.com/questions/45452935/pandas-how-to-get-series-to-dict
    dictionaries = [dict(key=re.findall(r'[0-9]+[.]?[0-9]*', str(k))[0], value=v) for k, v in firtRowDf.items()]
    #print(data)
    
    # 轉換成dataframe
    data = []
    headers = ['本益比-級距1倍數', '本益比-級距1價格', 
               '本益比-級距2倍數', '本益比-級距2價格',
               '本益比-級距3倍數', '本益比-級距3價格',
               '本益比-級距4倍數', '本益比-級距4價格',
               '本益比-級距5倍數', '本益比-級距5價格', 
               '本益比-級距6倍數', '本益比-級距6價格']
    for entry in dictionaries:
        #print(entry)
        data.append(entry['key'])
        data.append(entry['value'])

    ##print(headers)
    #print(data)
    df = pd.DataFrame([data], columns=headers)
    return df

'''
# 測試
data = GetPE('2474')
print(data)
'''