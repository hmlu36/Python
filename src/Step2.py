import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import random
import requests
import re
from lxml import etree
from decimal import Decimal
from BbrowserUserAgent import GetHeader

'''
選股條件：
1. 本益比小於10
2. 小於近五年本益比第1項
'''
def GetPE(stockId):
    url = f'https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stockId}&CHT_CAT=WEEK'
    resInfo = requests.get(url, headers=GetHeader())
    resInfo.encoding = 'utf-8'
    htmlInfo = etree.HTML(resInfo.text)

    header = ['EPS', 'PE_now']
    for index in range(1, 6, 1):
        XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[142]/td[{index}]/nobr'
        entry = htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]
        header.append(entry)
    #print(header)

    data = []
    for index in range(5, 12, 1):
        #print(index)
        XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[3]/td[{index}]'
        #print(XPath)

        entry = htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]
        data.append(entry)

    #print(data)
    PE = {}
    for index in range(len(header)):
        #print(header[index] + ': ' + data[index])
        PE.update({header[index] : data[index]})
    return PE