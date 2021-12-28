from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time
from datetime import datetime

def GetDividend(stockId):
    url = f'https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID={stockId}'
    cssSelector = '#divDetail'
    try:
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(3)
    except:
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(3)

    # column replace space
    df.columns = df.columns.str.replace(' ', '')

    # filter not  ∟
    df = df[df['股利發放年度'] != '∟']
    #print(df)

    # 年度大於2022, 移除第一列
    firstRow = df.iloc[0, :]
    if int(firstRow['股利發放年度']) > datetime.now().year:
        df = df.iloc[1: , :]

    rowsCount = 5
    # 年度(取前5筆, index重新排序)
    year = pd.to_numeric(df.iloc[:, 0], errors='coerce').dropna(how='any',axis=0).head(rowsCount).astype(int).reset_index(drop=True)
    #print(year)

    # 現金(取前5筆, index重新排序)
    cash = pd.to_numeric(df.iloc[:, 3], errors='coerce').dropna(how='any',axis=0).head(rowsCount).reset_index(drop=True)
    #print(cash)
    
    # 股票(取前5筆, index重新排序)
    stock = pd.to_numeric(df.iloc[:, 6], errors='coerce').dropna(how='any',axis=0).head(rowsCount).reset_index(drop=True)
    #print(stock)

    data = []
    for index in range(0, rowsCount):
        data.append(str(cash[index]).rjust(6) + ' / ' + str(stock[index]).rjust(6))

    print(data)
    df = pd.DataFrame([data], columns=year)
    
    return df
    '''
    data = pd.to_numeric(df['＞1千張'], errors='coerce').dropna(how='any',axis=0).head(3)
    return ' / '.join(map(str, list(data)))
'''

df = GetDividend('2356')
print(df)
