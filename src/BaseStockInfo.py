
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import random
import requests
import re
from lxml import etree
from decimal import Decimal


def GetCompetitor():
    # ----------------- （１）評估價值是否被低估？（股票價格不會太貴） -------------
    ########## 去公開資訊觀測站，把本益比、股價淨值比爬下來 ##########
    url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_=' + str(time.time())
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson = json.loads(soup.text)

    # 因為是表格式，用dataframe處理會比較方便
    stockdf = pd.DataFrame(getjson['data'], columns=["證券代號", "證券名稱", "殖利率(%)", "股利年度", "本益比", "股價淨值比", "財報年/季"])
    
    #del stockdf['證券名稱']

    PBR = pd.to_numeric(stockdf['股價淨值比'], errors='coerce') < 0.8  # 找到股價淨值比小於0.7的股票
    PER = pd.to_numeric(stockdf['本益比'], errors='coerce') < 10  # 找到本益比小於10的股票
    DividendYield = pd.to_numeric(stockdf['殖利率(%)'].replace('-', 0), errors='coerce') > 5  # 殖利率 > 5

    candidate = stockdf[(PER & DividendYield)]  # 綜合以上兩者，選出兩者皆符合的股票
    #print(candidate)
    return candidate



def GetStockCapital():
    df = pd.read_csv('https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv')
    # print(df)

    #data = df.set_index("公司代號")["上市日期"].to_dict()
    df[['公司代號', '上市日期']] = df[['公司代號', '上市日期']].astype(str)

    # rename dataframe specific column name
    # ref: https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
    return df[['公司代號', '公司名稱', '實收資本額', '上市日期']].rename(columns = {'公司代號':'證券代號'})

    # print(data)
    # return data

def GetStockInfo():
    competitor = GetCompetitor()
    capital = GetStockCapital()
    # merge dataframe
    # ref: http://violin-tao.blogspot.com/2017/06/pandas-2-concat-merge.html
    return pd.merge(competitor, capital, on='證券代號')

'''
# 測試
competitors = GetCompetitor()
print(competitors)
data = GetStockCapital()
print(data.loc[data['公司代號'] == '2069'])
'''

# 測試
data = GetStockInfo()
print(data)