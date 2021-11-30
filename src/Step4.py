import pandas as pd
from bs4 import BeautifulSoup
import time
from io import StringIO
import random
import requests
from lxml import etree
from decimal import Decimal
from BbrowserUserAgent import GetHeader
from Utils import GetDataByXPath

'''
上市公司基本資料 取得上市日期
'''

def GetListingDate():
    df = pd.read_csv('https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv')
    #print(df)
    data = df.set_index("公司代號")["上市日期"].to_dict()
    #print(data)
    return data

'''
# 測試
data = GetListingDate()
'''