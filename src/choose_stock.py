
import pandas as pd
from bs4 import BeautifulSoup
import time
from io import StringIO
import random
from lxml import etree
import twstock
from decimal import Decimal
from Step1 import GetCompetitor
from Step2 import GetPE
from Step3 import GetStockInfo
from Step4 import GetStockCapital
import Utils
import csv

'''
選股條件：
（1）評估價值是否被低估？（股票價格不會太貴）
1. 本益比　　　< 15倍
2. 現金殖利率　> 5 %

（2）本益比低估
1. 本益比小於10
2. 小於近五年最小級距本益比

（3）確定本業利益是成長的，且為本業賺的（不是靠業外收益賺的，獲利不持久）
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10
'''
        
championStock = {}

competitors = GetCompetitor()
stockCapital = GetStockCapital()

#print(competitors)
#print(stockInfo)
with open('參考清單.csv', 'w', newline='') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow([
                        '公司名稱', '股本(億)', '上市日期', '成交價', '殖利率(%)', '本益比', '股價淨值比', 
                        '營收累計年增率', '毛利率', '營業利益率', '稅前淨利率', '稅後淨利率', '本業收益', 'ROE', '董監持股比', 
                        '本益比-級距1', '本益比-級距2', '本益比-級距3', '本益比-級距4', '本益比-級距5', '本益比-級距6'
                     ])

    for stockId in competitors['證券代號']:
        entryStockCapital = stockCapital.loc[stockCapital['公司代號'] == stockId]
        stockName = entryStockCapital['公司名稱'].values[0]
        #print(competitors.loc[competitors['證券代號'] == stockId])
        print(stockName + '(' + stockId + ')')
        shareCapital = round(entryStockCapital['實收資本額'].values[0] / 100000000, 4)
        print('股本:' + str(shareCapital))
        #time.sleep(random.randint(0, 10))

        listingDate = entryStockCapital['上市日期'].values[0]
        print('上市日期:' + listingDate + ':' + str(Utils.GetYearBetween(listingDate)))
        
        # 大於等於5年的上市公司
        if Utils.GetYearBetween(listingDate) >= 5:
            entryCompetitor = competitors[competitors['證券代號'] == stockId]
            dividendYield = entryCompetitor['殖利率(%)'].values[0]
            print("殖利率:" + dividendYield)

            PE = entryCompetitor['本益比'].values[0]
            print('本益比:' + PE)

            PBR = entryCompetitor['股價淨值比'].values[0]
            print('股價淨值比:' + PBR)

            #stock = twstock.Stock(stockId)
            #print("目前價格:" + str(stock.price[-1:][0]))
            stockInfo = GetStockInfo(stockId)
            currentPrice = stockInfo['成交價']
            print("目前價格:" + currentPrice)

            target1 = stockInfo['營收累計年增率']
            print("營收累計年增率:" + target1)

            target2 = stockInfo['毛利率']
            print("毛利率:" + target2)
            
            target3 = stockInfo['營業利益率']
            print("營業利益率:" + target3)

            target4 = stockInfo['稅前淨利率']
            print("稅前淨利率:" + target4)
            
            target5 = stockInfo['稅後淨利率']
            print("稅後淨利率:" + target5)
            
            target6 = stockInfo['本業收益']
            print("本業收益:" + target6)
            
            target7 = stockInfo['ROE']
            print("ROE:" + target7)
            
            target8 = stockInfo['董監持股']
            print("董監持股:" + target8)

            #毛利率 > 0, 本業收益 > 0, ROE > 10
            if Decimal(target2) > 0 and Decimal(target6) > 0 and Decimal(target7) > 10:
                PEInfo = GetPE(stockId) 
                print(PEInfo)

                writer.writerow([
                                    stockName + '(' + stockId + ')', shareCapital, listingDate, currentPrice, dividendYield, PE, PBR, 
                                    target1, target2, target3, target4, target5, target6, target7, target8, 
                                    list(PEInfo)[2] + ' / ' + list(PEInfo.values())[2], list(PEInfo)[3] + ' / ' + list(PEInfo.values())[3], 
                                    list(PEInfo)[4] + ' / ' + list(PEInfo.values())[4], list(PEInfo)[3] + ' / ' + list(PEInfo.values())[5], 
                                    list(PEInfo)[6] + ' / ' + list(PEInfo.values())[6]
                                ])
                            
        
        time.sleep(random.randint(15, 20))
        