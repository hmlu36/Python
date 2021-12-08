import requests
import json
import pandas as pd
import datetime
import calendar
import time
import browserUserAgent
from bs4 import BeautifulSoup
import numpy as np
import twstock


# 抓取表格資料, 顯示出來
def GetSma(stockId):
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID="
    res = requests.get(url + stockId, headers=browserUserAgent.GetHeader())
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")

    ma5 = soup.select_one("body > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > div:nth-child(6) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
    print(ma5)
    # print(table)

stock_2330 = twstock.Stock('2330')
price_2330 = stock_2330.price[-5:]
print(price_2330)
#print(CalculateSma(df, 5))
#print(CalculateSma(df, 20))
#print(CalculateSma(df, 60))
#df = GetSma('2330')
# print(df)
