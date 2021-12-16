import pandas as pd
from bs4 import BeautifulSoup
import time
from io import StringIO
import random
import requests
from lxml import etree
from decimal import Decimal
from BrowserUserAgent import GetHeader
from Utils import GetDataByXPath

'''
上市公司基本資料 取得上市日期、股本
'''


def GetStockCapital():
    df = pd.read_csv('https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv')
    # print(df)

    #data = df.set_index("公司代號")["上市日期"].to_dict()
    df[['公司代號', '上市日期']] = df[['公司代號', '上市日期']].astype(str)
    return df[['公司名稱', '公司代號', '實收資本額', '上市日期']]

    # print(data)
    # return data


'''
# 測試
data = GetStockCapital()
print(data.loc[data['公司代號'] == '2069'])
'''
