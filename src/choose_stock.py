
import pandas as pd
import time
from io import StringIO
from decimal import Decimal
import random

from Step1_BasicStockInfo import GetBasicStockInfo
from Step2_FinDetail import GetFinDetail
from Step3_K_ChartFlow import GetPE
from Step4_K_Chart import GetTransaction
from Step6_StockDividendPolicy import GetDividend
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
        competitors = GetBasicStockInfo(True)
        #print(competitors)
        competitors.to_csv('過濾清單.csv',encoding='utf_8_sig')

    # 明細資料
    if op == 2:
        basicStockInfo_df = GetBasicStockInfo()
        sum_df = pd.DataFrame()
        for stockId in ['1474','1514','1515','1587','2020','2069','2347','2458','2520','2546','2881','3706','5515','8112','8150','8213']: #'5515', '2020', '2546', '2881', '2385', '2069', '2458', '2347', '3005', '3706', '1229', '1231', '3044'
            print(stockId)
            
            stockInfo_df = basicStockInfo_df[basicStockInfo_df['證券代號'] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)
            
            finDetail_df = GetFinDetail(stockId)
            print(finDetail_df)

            time.sleep(random.randint(20, 30))
            PE_df = GetPE(stockId)
            print(PE_df)

            time.sleep(random.randint(20, 30))
            transaction_df = GetTransaction(stockId)
            print(transaction_df)
            
            time.sleep(random.randint(20, 30))
            dividend_df = GetDividend(stockId)
            print(dividend_df)
            
            temp_df = pd.concat([stockInfo_df, transaction_df, PE_df, finDetail_df, dividend_df], axis=1)
            print(temp_df)

            # 合併所有欄位成一列
            sum_df = pd.concat([sum_df, temp_df], axis=0)

        #將列合併入dataframe
        sum_df.to_csv('彙整清單.csv',encoding='utf_8_sig')
            
# 1 產生過濾清單
# 2 抓出股票明細資料
GetChampionStock(2)
