import pandas as pd
from decimal import Decimal
import Utils
from BrowserUserAgent import GetHeader
import requests
from bs4 import BeautifulSoup
import time
import random
'''
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10 %
8. 董監持股比例 > 20
'''


def GetFinHeaders():
    return ['毛利率', '營業利益率', '股東權益報酬率  (年預估)', '稅前淨利率', '稅後淨利率', '總資產週轉率', '本業收益', '每股營業現金流量', '每股自由現金流量', '財報評分']


def GetFinDetail(stockId):
    url = f'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stockId}'
    css_selector = '#txtFinBody'
    try:
        df = Utils.GetDataFrameByCssSelector(url, css_selector)
    except:        
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, css_selector)
    #print(df)

    dict = {}

    headers = GetFinHeaders()
    for header in headers:
        if header == '本業收益':
            try:
                # 本業收益（營業利益率／稅前淨利率） > ６０％
                tempDict = round(Decimal(dict['營業利益率']) / Decimal(dict['稅前淨利率']) * 100, 2)
                dict.update({'本業收益': str(tempDict)})
            except:
                dict.update({'本業收益': '0'})
        else:
            try:
                #print(header)
                tempDict = Utils.GetDataFrameValueByLabel(df, '獲利能力', header)
                dict.update({header.replace('股東權益報酬率  (年預估)', 'ROE') : str(Decimal(tempDict[0]))})
            except:
                dict.update({header.replace('股東權益報酬率  (年預估)', 'ROE') : '0'})

    df = pd.DataFrame([dict])
    
    return df

'''
# 測試
data = GetFinDetail("8150")
print(data)
'''