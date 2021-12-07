
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
from Step3 import GetIncome
from Step4 import GetListingDate
import Utils

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
listingDate = GetListingDate()

print(competitors)
for stockId in competitors["證券代號"]:
    time.sleep(random.randint(0, 10))
    name = competitors.loc[competitors['證券代號'] == stockId, '證券名稱'].values[0]
    stockKistingDate = listingDate.get(Decimal(stockId))
    if Utils.GetYearBetween(stockKistingDate) < 3:
        continue

    print(str(stockKistingDate))
    print(name + " (" + stockId + ") ")

    PE = GetPE(stockId)
    #print(PE)
    stock = twstock.Stock(stockId)
    print("現今本益比:" + PE['CurrentPE'])
    print("目前價格:" + str(stock.price[-1:][0]))
    print("推估最低本益比價格:" + list(PE.values())[2])

    Income = GetIncome(stockId)
    print(Income)

    # 本益比 < 10, 目前股價小於最小級距本益比
    if Decimal(PE['CurrentPE']) < 10 and stock.price[-1:][0] < Decimal(list(PE.values())[2]):
        '''
            1. 營收累計年增率 > 0 %
            2. 毛利率 > 0 %
            3. 營業利益率 > 0 %
            4. 稅前淨利率 > 0 %
            5. 稅後淨利率 > 0 %
            6. 本業收益（營業利益率／稅前淨利率） > 50 %
            7. ROE > 10
        '''
        if Decimal(Income["營收累計年增率"]) > 0 and Decimal(Income["毛利率"]) > 0 and Decimal(Income["營業利益率"]) > 0 and Decimal(Income["稅前淨利率"]) > 0 and Decimal(Income["本業收益"]) > 50 and Decimal(Income["ROE"]) > 10:
            print("冠軍股:" + stockId)
            championStock.update({name: stockId})
    print()

print(championStock)