import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import random
import requests
import re
from lxml import etree
from decimal import Decimal
from BrowserUserAgent import GetHeader
from Utils import GetDataByXPath
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
    resInfo = requests.get(url, headers = GetHeader())
    resInfo.encoding = 'utf-8'
    htmlInfo = etree.HTML(resInfo.text)

    header = ['EPS', 'CurrentPE']
    for index in range(1, 7, 1):
        #2115
                #/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[3]/td[5]
        XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[142]/td[{index}]/nobr'
        target = GetDataByXPath(htmlInfo, XPath)
        header.append(target)
    #print(header)

    entry = []
    for index in range(5, 13, 1):
        #print(index)
        XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[3]/td[{index}]'
        #print(XPath)

        target = GetDataByXPath(htmlInfo, XPath)
        entry.append(target)

    #print(entry)
    data = {}
    for index in range(len(header)):
        #print(header[index] + ': ' + data[index])
        data.update({header[index] : entry[index]})
    return data


# 測試
data = GetPE("3702")
print(data)
print(list(data)[2] + ' / ' + list(data.values())[2])
