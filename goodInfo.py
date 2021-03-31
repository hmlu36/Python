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

stocks = [  '2923', '2929', '2936', '2939', '3002', '3003', '3004', '3005', '3006', '3008', '3010', '3011', '3013', '3014', '3015', '3016', '3017', '3018', '3019', '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3035', '3036', '3037', '3038', '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048', '3049', '3050', '3051', '3052', '3054', '3055', '3056', '3057', '3058', '3059', '3060', '3062', '3090', '3094', '3130', '3138', '3149', '3164', '3167', '3189', '3209', '3229', '3231', '3257', '3266', '3296', '3305', '3308', '3311', '3312', '3321', '3338', '3346', '3356', '3376', '3380', '3383', '3406', '3413', '3416', '3419', '3432', '3437', '3443', '3450', '3454', '3481', '3494', '3501', '3504', '3515', '3518', '3528', '3530', '3532', '3533', '3535', '3536', '3543', '3545', '3550', '3557', '3563', '3576', '3583', '3588', '3591', '3593', '3596', '3605', '3607', '3617', '3622', '3645', '3653', '3661', '3665', '3669', '3673', '3679', '3682', '3686', '3694', '3701', '3702', '3703', '3704', '3705', '3706', '3708', '3711', '3712', '3714', '4104', '4106', '4108', '4119', '4133', '4137', '4141', '4142', '4148', '4155', '4164', '4190', '4306', '4414', '4426', '4438', '4439', '4526', '4532', '4536', '4540', '4545', '4551', '4552', '4555', '4557', '4560', '4562', '4564', '4566', '4571', '4572', '4576', '4581', '4720', '4722', '4737', '4739', '4746', '4755', '4763', '4764', '4766', '4807', '4904', '4906', '4912', '4915', '4916', '4919', '4927', '4930', '4934', '4935', '4938', '4942', '4943', '4952', '4956', '4958', '4960', '4961', '4967', '4968', '4976', '4977', '4989', '4994', '4999', '5007', '5203', '5215', '5225', '5234', '5243', '5258', '5269', '5283', '5284', '5285', '5288', '5388', '5434', '5469', '5471', '5484', '5515', '5519', '5521', '5522', '5525', '5531', '5533', '5534', '5538', '5546', '5607', '5608', '5706', '5871', '5876', '5880', '5906', '5907', '6005', '6024', '6108', '6112', '6115', '6116', '6117', '6120', '6128', '6133', '6136', '6139', '6141', '6142', '6152', '6153', '6155', '6164', '6165', '6166', '6168', '6172', '6176', '6177', '6183', '6184', '6189', '6191', '6192', '6196', '6197', '6201', '6202', '6205', '6206', '6209', '6213', '6214', '6215', '6216', '6224', '6225', '6226', '6230', '6235', '6239', '6243', '6251', '6257', '6269', '6271', '6277', '6278', '6281', '6282', '6283', '6285', '6288', '6289', '6405', '6409', '6412', '6414', '6415', '6416', '6426', '6431', '6438', '6442', '6443', '6449', '6451', '6456', '6464', '6477', '6491', '6504', '6505', '6515', '6525', '6531', '6533', '6541', '6552', '6558', '6573', '6579', '6581', '6582', '6591', '6592', '6598', '6605', '6625', '6641', '6655', '6666', '6668', '6669', '6670', '6671', '6672', '6674', '6698', '6706', '6715', '6743', '6754', '6756', '6781', '8011', '8016', '8021', '8028', '8033', '8039', '8046', '8070', '8072', '8081', '8101', '8103', '8104', '8105', '8110', '8112', '8114', '8131', '8150', '8163', '8201', '8210', '8213', '8215', '8222', '8249', '8261', '8271', '8341', '8367', '8374', '8404', '8411', '8422', '8427', '8429', '8442', '8443', '8454', '8462', '8463', '8464', '8466', '8467', '8473', '8478', '8480', '8481', '8482', '8488', '8499', '8926', '8940', '8996', '9802', '9902', '9904', '9905', '9906', '9907', '9908', '9910', '9911', '9912', '9914', '9917', '9918', '9919', '9921', '9924', '9925', '9926', '9927', '9928', '9929', '9930', '9931', '9933', '9934', '9935', '9937', '9938', '9939', '9940', '9941', '9942', '9943', '9944', '9945', '9946', '9955', '9958']

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
