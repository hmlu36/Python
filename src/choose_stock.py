
import pandas as pd
import time
from io import StringIO
from decimal import Decimal
import random

from Step1_BaseStockInfo import GetBaseStockInfo
from Step2_FinDetail import GetFinDetail
from Step3_K_ChartFlow import GetPE
from Step4_K_Chart import GetTransaction
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
def GetChampionStock(op):
    # 過濾清單
    if op == 1:
        competitors = GetBaseStockInfo()
        #print(competitors)
        competitors.to_csv('過濾清單.csv',encoding='utf_8_sig')

    # 明細資料
    if op == 2:
        for stockId in ['2474']:
            print(stockId)
            data = GetFinDetail(stockId)
            print(data)

            time.sleep(random.randint(20, 30))
            data = GetPE(stockId)
            print(data)

            time.sleep(random.randint(20, 30))
            data = GetTransaction(stockId)
            print(data)

            
# 1 產生過濾清單
# 2 抓出股票明細資料
GetChampionStock(2)
