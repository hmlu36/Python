
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
from datetime import datetime, timedelta

def GetDailyExchangeReport(filter):
    # ----------------- （１）評估價值是否被低估？（股票價格不會太貴） -------------
    ########## 去公開資訊觀測站，把本益比、股價淨值比爬下來 ##########
    url = f'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_={str(time.time())}'
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson = json.loads(soup.text)

    # 因為是表格式，用dataframe處理會比較方便
    stockdf = pd.DataFrame(getjson['data'], columns=["證券代號", "證券名稱", "殖利率(%)", "股利年度", "本益比", "股價淨值比", "財報年/季"])
    
    del stockdf['財報年/季']
    del stockdf['股利年度']

    stockdf = stockdf.rename(columns = {'殖利率(%)':'殖利率', '股價淨值比':'淨值比'})

    if filter:
        #errors = 'coerce'：是因為本益比千位數有逗號，若改成value會出錯，這個指令是讓出錯的地方以NaN型式取代
        PBR = pd.to_numeric(stockdf['淨值比'], errors='coerce') < 0.8  # 找到股價淨值比小於0.7的股票
        PER = pd.to_numeric(stockdf['本益比'], errors='coerce') < 10  # 找到本益比小於10的股票
        DividendYield = pd.to_numeric(stockdf['殖利率'].replace('-', 0), errors='coerce') > 3  # 殖利率 > 3

        candidate = stockdf[(PER & DividendYield)]  # 綜合以上兩者，選出兩者皆符合的股票
        #print(candidate)
        return candidate
    else:
        return stockdf

        
# 取出每日收盤價
def GetDailyExchange():
    url = 'https://quality.data.gov.tw/dq_download_json.php?nid=11549&md5_url=da96048521360db9f23a2b47c9c31155'
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df[['證券代號', '收盤價']]
    return df

# 資本額
def GetStockCapital(filter):
    df = pd.read_csv('https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv')
    # print(df)
    
    if filter:
        # 大於等於5年的上市公司
        fiveYearBefore = (datetime.today() - timedelta(days=5 * 365)).strftime('%Y%m%d')
        #print(fiveYearBefore)
        YEAR_CONDITION = pd.to_datetime(df['上市日期'], format='%Y%m%d') < fiveYearBefore 
        df = df[YEAR_CONDITION]        

    #data = df.set_index("公司代號")["上市日期"].to_dict()
    df[['公司代號', '成立日期', '上市日期']] = df[['公司代號', '成立日期', '上市日期']].astype(str)

    # rename dataframe specific column name
    # ref: https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
    return df[['公司代號', '公司名稱', '實收資本額', '成立日期', '上市日期']].rename(columns = {'公司代號':'證券代號'})

    # print(data)
    # return data

def GetBasicStockInfo(filter=False):

    exchangeReport = GetDailyExchangeReport(filter)

    capital = GetStockCapital(filter)

    # merge dataframe
    # ref: http://violin-tao.blogspot.com/2017/06/pandas-2-concat-merge.html
    mergeDf = pd.merge(capital, exchangeReport, on='證券代號')

    # move column in pandas dataframe
    # ref https://stackoverflow.com/questions/35321812/move-column-in-pandas-dataframe
    column_to_move = mergeDf.pop("證券名稱")
    mergeDf.insert(1, "證券名稱", column_to_move)
    #print(mergeDf)

    if filter:
        dailyExhange_df = GetDailyExchange()
        mergeDf = pd.merge(mergeDf, dailyExhange_df, on='證券代號')

    # 董監持股比例
    directShareHold_df = pd.read_csv('Data\Monthly\董監持股比例.csv')
    directShareHold_df = directShareHold_df.rename(columns = {'代號':'證券代號', '全體  董監  持股  (%)':'全體董監持股(%)'})
    #print(directShareHold_df)
    directShareHold_df = directShareHold_df[['證券代號', '全體董監持股(%)']].astype(str)
    mergeDf = pd.merge(mergeDf, directShareHold_df, on='證券代號')

    # 股東分布資料
    shareHoder_df = pd.read_csv('Data\Weekly\股東分布資料.csv')
    shareHoder_df['100-1000張人數'] = shareHoder_df[['101-200張人數', '201-400張人數', '401-800張人數', '801-1000張人數']].sum(axis=1)
    shareHoder_df['100-1000張比例'] = shareHoder_df[['101-200張人數', '201-400張人數', '401-800張人數', '801-1000張人數']].sum(axis=1)
    shareHoder_df = shareHoder_df[['證券代號', '100張以下人數', '100張以下比例', '100-1000張人數', '100-1000張比例', '1000張以上人數', '1000張以上比例']].astype(str)
    mergeDf = pd.merge(mergeDf, shareHoder_df, on='證券代號')

    
    return mergeDf

'''
# 測試
df = GetBasicStockInfo()
print(df)
'''