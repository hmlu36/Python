
import pandas as pd
import time
from io import StringIO
from decimal import Decimal
import random

import requests

from Step1_BasicStockInfo import GetBasicStockInfo
from Step2_FinDetail import GetFinDetail
from Step3_K_ChartFlow import GetPE
from Step4_K_Chart import GetTransaction
import Step5_ShareholderDistribution as shareholderDistribution
from Step6_StockDividendPolicy import GetDividend
import Step8_DirectorSharehold as directorSharehold
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
def Sleep():
    time.sleep(random.randint(30, 60))

def GetChampionStock(op):
    # 過濾清單
    if op == 0:
        competitors = GetBasicStockInfo(True)
        #print(competitors)
        competitors.to_csv('Data\Temp\過濾清單.csv',encoding='utf_8_sig')

    if op == 1:   
        basicStockInfo_df = GetBasicStockInfo()
        
        for stockId in ['2477']:
            PE_df = GetPE(stockId)
            print(PE_df)
            
            Sleep()
            stockInfo_df = basicStockInfo_df[basicStockInfo_df['證券代號'] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)

            temp_df = pd.concat([stockInfo_df, PE_df], axis=1)
            temp_df.to_csv('Data\Temp\過濾清單(含本益比).csv', mode='a', header=False, encoding='utf_8_sig')

    # 明細資料
    if op == 2:
        basicStockInfo_df = GetBasicStockInfo()
        sum_df = pd.DataFrame()
        for stockId in ['2467']: #'5515', '2020', '2546', '2881', '2385', '2069', '2458', '2347', '3005', '3706', '1229', '1231', '3044'
            print(stockId)
            
            stockInfo_df = basicStockInfo_df[basicStockInfo_df['證券代號'] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)
            
            Sleep()
            finDetail_df = GetFinDetail(stockId)
            print(finDetail_df)

            PE_df = GetPE(stockId)
            print(PE_df)

            Sleep()
            transaction_df = GetTransaction(stockId)
            print(transaction_df)
            
            Sleep()
            dividend_df = GetDividend(stockId)
            print(dividend_df)
            
            
            Sleep()
            distribution_df = shareholderDistribution.GetDistribution(stockId)
            print(distribution_df)
            
            # 合併所有欄位成一列
            temp_df = pd.concat([stockInfo_df, transaction_df, PE_df, finDetail_df, dividend_df, distribution_df], axis=1)
            print(temp_df)

            #將列合併入dataframe
            #sum_df = pd.concat([sum_df, temp_df], axis=0)
            
            # 每列寫入csv檔, 不含表頭
            temp_df.to_csv('彙整清單.csv', mode='a', header=False, encoding='utf_8_sig')
        
        # 寫入csv檔
        #sum_df.to_csv('彙整清單.csv', encoding='utf_8_sig')

    # 日常籌碼面資料
    if op == 3:
        basicStockInfo_df = GetBasicStockInfo()
        #sum_df = pd.DataFrame()
        for stockId in ['1229', '1231', '1409', '1474', '1514', '1515', '1587', '2020', '2069', '2324', '2347', '2352', '2385', '2417', '2458', '2520', '2546', '2881', '3005', '3044', '3209', '3702','3706', '5515', '6257', '8112', '8150', '8213', '8215', '2467']:
 
            stockInfo_df = basicStockInfo_df[basicStockInfo_df['證券代號'] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)
            
            Sleep()
            transaction_df = GetTransaction(stockId)
            print(transaction_df)

            temp_df = pd.concat([stockInfo_df, transaction_df], axis=1)
            print(temp_df)
            
            temp_df.to_csv('籌碼面資料.csv', mode='a', header=False, encoding='utf_8_sig')
            # 合併所有欄位成一列
            #sum_df = pd.concat([sum_df, temp_df], axis=0)

        #將列合併入dataframe
        #sum_df.to_csv('籌碼面資料.csv',encoding='utf_8_sig')
    
    if op == 4:
        shareholderDistribution.WriteData()
    
    if op == 5:
        directorSharehold.WriteData()
          
# 0 產生過濾清單(本益比、殖利率、淨值比、收盤價、全體董監持股、股東分布人數)
# 1 產生過濾清單(同0含本益比)
# 2 抓出股票明細資料
# 3 日排程 - 籌碼面資料
# 4 週排程 - 大戶、本益比
# 5 月排程 - 董監比例
# 6 季排程 - 財務資料
GetChampionStock(0)
