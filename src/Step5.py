import pandas as pd
from bs4 import BeautifulSoup
import time
from io import StringIO
import random
import requests
from lxml import etree
from decimal import Decimal
from Utils import GetDataByXPath
from BbrowserUserAgent import GetHeader

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
def GetPageContent(url):
    print(url)

    # 要睡覺一下，不然會被ben掉
    time.sleep(random.randint(15, 60))

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
        

def GetStockInfo(stockId):
    url = f"https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID={stockId}"
    rawData = requests.get(url, headers = GetHeader())
    rawData.encoding = 'utf-8'
    soup = BeautifulSoup(rawData.text, "html.parser")

    table = soup.find('table', attrs={'class':'b1 p4_4 r0_10 row_mouse_over'})
    table_rows = table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    
    print(res)
    data = {}
    
    '''
    # 成交價
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[3]/td[1]"
    currentPrice = GetDataByXPath(htmlInfo, XPath)
    print('成交價:' + currentPrice)
    data.update({'成交價': currentPrice})

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

    time.sleep(random.randint(15, 30))
    url = f"https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stockId}"
    resInfo2 = requests.get(url, headers = GetHeader())
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
    
    # 董監持股
    XPath = "/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[1]/div[7]/div/table/tbody/tr[4]/td[3]/nobr"
    target8 = GetDataByXPath(htmlInfo, XPath)
    print('董監持股:' + target8)
    data.update({'董監持股': target8})

    #每股營業現金流量
    try:
        XPath = '/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[100]/td[2]/nobr'
        target9 = GetDataByXPath(htmlInfo2, XPath)
    except: 
        XPath = '/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[90]/td[2]/nobr'
        target9 = GetDataByXPath(htmlInfo2, XPath)
    print('每股營業現金流量:' + target9)
    data.update({'每股營業現金流量': target9})  
  
    #每股自由現金流量
    # 1423 利華的位置不一樣
    try:
        XPath = '/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[104]/td[2]/nobr'
        target10 = GetDataByXPath(htmlInfo2, XPath)
    except:    
        XPath = '/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[98]/td[1]/nobr'
        target10 = GetDataByXPath(htmlInfo2, XPath)
    
    if target10.isnumeric() == False:
        XPath = '/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[94]/td[2]/nobr'
        target10 = GetDataByXPath(htmlInfo2, XPath)
        
    print('每股自由現金流量:' + target10)
    data.update({'每股自由現金流量': target10})
    '''
    return data

# 測試
data = GetStockInfo("2546")
print(data)
