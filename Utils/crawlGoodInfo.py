import time
from pony.orm import *
from bs4 import BeautifulSoup
import sys
sys.path.append('../')
from Models.settings import db
import requests
import json
import pandas as pd
import numpy as np
import sqlite3
import re
import browserUserAgent


# 抓取表格資料, 顯示出來
def CrawlStockDetail(stockId):
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID="
    res = requests.get(url + stockId, headers=browserUserAgent.GetHeader())
    res.encoding = "utf-8"
    return BeautifulSoup(res.text, "lxml")


def GetGridData(soup, cssSelector, titleIndex, dataType):
    table = soup.select_one(cssSelector)
    # print(table)

    # 標題
    '''
       columns = [td.text.replace('\n', '')
                  for td in table.find_all('tr')[titleIndex].find_all('td')]
    # print(columns)
    '''

    # 內容
    rows = list()

    # 判斷取得明細或股利, 筆數不一訂滿10筆
    # 股利要扣掉最後一筆說明 (ex: 1341)
    tempTopRecord = (len(table.find_all('tr')) - titleIndex - 1)
    if dataType == 'dividend':
        tempTopRecord -= 1
    print(tempTopRecord)

    # 抓取第4筆以後的資料, 取前10筆
    for tr in table.find_all('tr')[(titleIndex + 1):][:tempTopRecord]:
        rows.append([re.findall('[^()]+', td.text.replace('\n', '').replace('\xa0', '').replace(',', '').replace('-', '0'))[0]  # 使用regular expression 取出括號前的值
                    for td in tr.find_all('td')])
        # print(rows)

    # df = pd.DataFrame(data=rows, columns=columns)
    # print(df)
    return rows


# 取得個股資訊
def GetCompanyInfo(soup):
    return [soup.select_one("table.solid_1_padding_4_4_tbl:nth-child(2) > tr:nth-child(1) > td:nth-child(2)").text,
            soup.select_one("table.solid_1_padding_4_4_tbl:nth-child(2) > tr:nth-child(2) > td:nth-child(2)").text]


# 抓取個股股利
def GetStockDividend(soup):
    return GetGridData(soup, '#FINANCE_DIVIDEND', 3, 'dividend')
    # print(table)B


# 抓取個股ROE、毛利等、EPS 等..明細
def GetStockDetail(soup):
    return GetGridData(soup, '#FINANCE_INCOME_M > div:nth-child(2) > div:nth-child(1) > table', 0, 'detail')


# 股海老牛選股
# stocks = ["1216", "1229", "1319", "1730", "2356", "2397", "2441", "2546", "2548",
#          "2882", "2884", "3036", "3402", "4506", "5871", "6024", "6196", "6202", "6279", "8926"]

stocks = [ '6781', '8011', '8016', '8021', '8028', '8033', '8039', '8046', '8070', '8072', '8081', '8101', '8103', '8104', '8105', '8110', '8112', '8114', '8131', '8150', '8163', '8201', '8210', '8213', '8215', '8222', '8249', '8261', '8271', '8341', '8367', '8374', '8404', '8411', '8422', '8427', '8429', '8442', '8443', '8454', '8462', '8463', '8464', '8466', '8467', '8473', '8478', '8480', '8481', '8482', '8488', '8499', '8926', '8940', '8996', '9802', '9902', '9904', '9905', '9906', '9907', '9908', '9910', '9911', '9912', '9914', '9917', '9918', '9919', '9921', '9924', '9925', '9926', '9927', '9928', '9929', '9930', '9931', '9933', '9934', '9935', '9937', '9938', '9939', '9940', '9941', '9942', '9943', '9944', '9945', '9946', '9955', '9958']

for idx, stockId in enumerate(stocks):
    print(stockId)
    # 休息一下再抓, 避免存取過於頻繁被擋
    time.sleep(np.random.randint({True: 0, False: 30}[idx == 0], 60))

    # 取得goodinfo資料
    soup = CrawlStockDetail(stockId)

    # 取得公司資訊
    companyInfo = GetCompanyInfo(soup)

    with db_session:

        stockInfo = db.StockInfo.get(stockId=stockId)
        if stockInfo is None:  # 判斷資料是否存在
            db.StockInfo(stockId=stockId,
                         name=companyInfo[0],
                         industry=companyInfo[1])
        else:
            stockInfo.stockId = stockId
            stockInfo.name = companyInfo[0]
            stockInfo.industry = companyInfo[1]

        # 取得公司股票明細
        stockDetails = GetStockDetail(soup)
        for index, entry in enumerate(stockDetails):
            stockDetail = db.StockDetail.get(
                stockId=stockId, yearSeason=entry[0])
            if stockDetail is None:  # 判斷資料是否存在, 不存在新增
                db.StockDetail(stockId=stockId,
                               yearSeason=entry[0],
                               revenue=entry[1],
                               profitAfterTax=entry[2],
                               grossMargin=entry[3],
                               operatingIncome=entry[4],
                               profitAfterTaxPercentage=entry[5],
                               roe=entry[6],
                               eps=entry[7])
            else:  # 存在, 更新資料
                stockDetail.stockId = stockId
                stockDetail.yearSeason = entry[0]
                stockDetail.revenue = entry[1]
                stockDetail.profitAfterTax = entry[2]
                stockDetail.grossMargin = entry[3]
                stockDetail.operatingIncome = entry[4]
                stockDetail.profitAfterTaxPercentage = entry[5]
                stockDetail.roe = entry[6]
                stockDetail.eps = entry[7]

        # 取得股利明細
        stockDividends = GetStockDividend(soup)
        for index, entry in enumerate(stockDividends):
            stockDividend = db.StockDividend.get(
                stockId=stockId, year=entry[0])
            if stockDividend is None:  # 判斷資料是否存在, 不存在新增
                db.StockDividend(stockId=stockId,
                                 year=entry[0],
                                 cashDividends=entry[1],
                                 stockDividends=entry[2],
                                 totalDividends=entry[3])
            else:
                stockDividend.stockId = stockId
                stockDividend.year = entry[0]
                stockDividend.cashDividends = entry[1]
                stockDividend.stockDividends = entry[2]
                stockDividend.totalDividends = entry[3]
