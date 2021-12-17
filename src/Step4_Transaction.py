import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from io import StringIO
import requests
import re
from lxml import etree
from datetime import date, timedelta

'''
reference: https://www.ptt.cc/bbs/Stock/M.1639061202.A.DDD.html
一、選股
1、日線：日交易量大於5日均量250%以上
2、月線：低基期且已出量
3、籌碼：主力大戶60%以上且連續上升

二、進場：日均線預估即將向上排列
1、接近日5MA先進15%操作資金
2、接近週5MA再進15%操作資金

三、出場
1、獲利：日線價格已遠離5MA(必定出量) 或 日成交量趨近中長期大量
2、虧損：負5% 或 日均線已向下排列
'''
'''
Stock 物件的屬性	 說明
price	 傳回近 31 天的收盤價 (單位=元) 串列
capacity	 傳回近 31 天的成交量 (單位=股) 串列
turnover	 傳回近 31 天的成交金額 (單位=元) 串列
transaction	 傳回近 31 天的成交筆數 (單位=筆) 串列
close	 傳回近 31 天的收盤價 (單位=元) 串列 (同 price)
change	 傳回近 31 天收盤價的漲跌幅 (單位=元) 串列 
open 	 傳回近 31 天的開盤價 (單位=元) 串列
low	 傳回近 31 天的最低價 (單位=元) 串列
high	 傳回近 31 天的最高價 (單位=元) 串列
date	 傳回近 31 天的交易日期 datetime 物件串列
sid	 傳回股票代號字串
data	 傳回近 31 天的 Stock 物件全部資料內容 (Data 物件) 串列
raw_data	 傳回近 31 天所擷取之原始資料串列
https://yhhuang1966.blogspot.com/2018/11/python-twstock.html
'''


def ComposeDfByDate(stockId, date):
    dateformate = '%Y%m%d'
    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date.strftime(dateformate)}&stockNo={stockId}'
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson = json.loads(soup.text)
    # print(getjson['data'])
    # print(getjson['fields'])
    return pd.DataFrame(data=getjson['data'], columns=getjson['fields'])

# 取60ma


def GetTransactionInfo(stockId):
    df = pd.DataFrame()
    tempDate = date.today()
    stockDf = ComposeDfByDate(stockId, tempDate)
    #while df.shape[0] < 60:
    print(df.shape[0])
    stockDf = ComposeDfByDate(stockId, tempDate)
    tempDate = date.today().replace(day=1) - timedelta(days=1)
    df.append(stockDf)
    print(df.shape[0])

    return df


data = GetTransactionInfo('8112')
print(data)
