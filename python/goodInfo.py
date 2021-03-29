import time
from pony.orm import *
from Models.settings import db
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import sqlite3
import re
from lxml import etree

# 建立虛擬的Header User agent清單,防止IP被鎖。可用fake-useragent套件創建隨機user agent
ua = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
      'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36']

headers = {
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    "user-agent": ua[np.random.randint(0, 10)]
}


# 抓取表格資料, 顯示出來
def CrawlStockDetail(stockId):
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID="
    res = requests.get(url + stockId, headers=headers)
    res.encoding = "utf-8"
    return BeautifulSoup(res.text, "lxml")


def GetGridData(soup, cssSelector, titleIndex, topRecord):
    table = soup.select_one(cssSelector)
    # print(table)

    # 標題
    '''
       columns = [td.text.replace('\n', '')
                  for td in table.find_all('tr')[titleIndex].find_all('td')]
                  '''
    # print(columns)

    # 內容
    rows = list()
    # 抓取第4筆以後的資料, 取前10筆
    for tr in table.find_all('tr')[(titleIndex + 1):][:topRecord]:
        rows.append([re.findall('[^()]+', td.text.replace('\n', '').replace('\xa0', ''))[0]  # 使用regular expression 取出括號前的值
                    for td in tr.find_all('td')])
        # print(rows)

    #df = pd.DataFrame(data=rows, columns=columns)
    # print(df)
    return rows


# 取得個股資訊
def GetCompanyInfo(soup):
    return [soup.select_one("table.solid_1_padding_4_4_tbl:nth-child(2) > tr:nth-child(1) > td:nth-child(2)").text,
            soup.select_one("table.solid_1_padding_4_4_tbl:nth-child(2) > tr:nth-child(2) > td:nth-child(2)").text]


# 抓取個股股利
def GetStockDividend(stockId):
    GetGridData(stockId, '#FINANCE_DIVIDEND', 3, 10)
    # print(table)


# 抓取個股ROE、毛利等、EPS 等..明細
def GetStockDetail(stockId):
    return GetGridData(stockId, '#FINANCE_INCOME_M > div:nth-child(2) > div:nth-child(1) > table', 0, 10)


def GetDailyTradePrice(stockId):
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=${date}&stockNo="
    res = requests.get(url + stockId, headers=headers)
    res.encoding = "utf-8"
    # print(res.text)

    # 讀取json檔
    data = json.loads(res.text)
    columns = data["fields"]
    # print(columns)

    df = pd.DataFrame(data=data["data"], columns=columns)
    print(df)


# GetStockDividend("2330")
# GetStockDividend("2546")
# CrawlStockDetail("2546")
# GetDailyTradePrice("4414")


with db_session:
    stocks = ["2546", "2520"]
    for stockId in stocks:
        time.sleep(np.random.randint(5, 15))  # 休息5~15秒再抓, 避免存取過於頻繁被擋

        soup = CrawlStockDetail(stockId)

        # 取得公司資訊
        companyInfo = GetCompanyInfo(soup)
        db.StockInfo(stockId=stockId,
                     name=companyInfo[0],
                     industry=companyInfo[1])

        # 取得公司股票明細
        stockDetails = GetStockDetail(soup)
        for entry in stockDetails:
            db.StockDetail(stockId=stockId,
                           yearSeason=entry[0],
                           revenue=entry[1],
                           profitAfterTax=entry[2],
                           grossMargin=entry[3],
                           operatingIncome=entry[4],
                           profitAfterTaxPercentage=entry[5],
                           roe=entry[6],
                           eps=entry[7])
