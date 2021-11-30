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
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10 %
'''
def GetPageContent(url):
    print(url)

    # 要睡覺一下，不然會被ben掉
    time.sleep(random.randint(0, 10))

    rawData = requests.get(url)
    rawData.encoding = 'big5'
    #print(rawData.text)
    #print(rawData.encoding) # 網頁encoding
    soup = BeautifulSoup(rawData.text, "html.parser")
    getdata = ""
    if soup.find('font') is None or soup.find('font').text != '檔案不存在!':
        print("content exists")
        getdata = pd.read_html(url)
    #print(getdata)
    return getdata
        

def GetIncome(stockId):
    url = f"https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID={stockId}"
    resInfo = requests.get(url, headers=GetHeader())
    resInfo.encoding = 'utf-8'
    htmlInfo = etree.HTML(resInfo.text)
    data = {}

    #營收累計年增率 > 0 %
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/div[2]/div/table/tbody/tr[3]/td[6]"
    target1 = GetDataByXPath(htmlInfo, XPath)
    #print('營收累計年增率:' + str(Decimal(target1)))
    data.update({'營收累計年增率': str(Decimal(target1))})

    #毛利率 > 0 %
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/div[4]/div/div/table/tbody/tr[3]/td[4]"
    target2 = GetDataByXPath(htmlInfo, XPath)
    if target2 == '-':
        target2 = "0"
    #print('毛利率:' + target2)
    data.update({'毛利率': target2})

    #營業利益率 > 0 %
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/div[4]/div/div/table/tbody/tr[3]/td[5]"
    target3 = GetDataByXPath(htmlInfo, XPath)
    if target3 == '-':
        target3 = "0"
    #print('營業利益率:' + target3)
    data.update({'營業利益率': target3})

    time.sleep(random.randint(0, 10))
    url = f"https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stockId}"
    resInfo2 = requests.get(url, headers=GetHeader())
    resInfo2.encoding = 'utf-8'
    htmlInfo2 = etree.HTML(resInfo2.text)

    #稅前淨利率 > 0 %
    XPath = "/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[4]/td[2]/nobr"
    target4 = GetDataByXPath(htmlInfo2, XPath)
    #print('稅前淨利率:' + target4)
    data.update({'稅前淨利率': target4})

    #稅後淨利率 > 0 %
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/div[4]/div/div/table/tbody/tr[3]/td[6]"
    target5 = GetDataByXPath(htmlInfo, XPath)
    #print('稅後淨利率:' + target5)
    data.update({'稅後淨利率': target5})

    #本業收益（營業利益率／稅前淨利率） > ６０％
    target6 = round(Decimal(target3) / Decimal(target4) * 100, 2)
    #print('本業收益（營業利益率／稅前淨利率）:' + str(target6))
    data.update({'本業收益': str(target6)})

    # ROE
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/div[4]/div/div/table/tbody/tr[3]/td[7]/nobr/div[1]"
    target7 = GetDataByXPath(htmlInfo, XPath)
    #print('ROE:' + target7)
    data.update({'ROE': target7})
    
    return data

'''
# 測試
data = GetIncome("2838")
print(data)
'''