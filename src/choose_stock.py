
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import random
import requests
import re
from lxml import etree
import twstock
from decimal import Decimal
from Step1 import GetCompetitor
from Step2 import GetPE

'''
選股條件：
（1）評估價值是否被低估？（股票價格不會太貴）
1. 本益比    ＜15倍
2. 現金殖利率 ＞5％

（2）本益比低估
1. 本益比小於10
2. 小於近五年最小級距本益比

（3）確定本業利益是成長的，且為本業賺的（不是靠業外收益賺的，獲利不持久）
1. 營收累計年增率 > ０％
2. 毛利率 > ０％
3. 營業益益率 > ０％
4. 稅前淨利率 > ０％
5. 稅後淨利率 > ０％
6. 本業收益（營業利益率／稅前淨利率） > ６０％
'''
        
competitors = GetCompetitor()
print(competitors)
for stockId in competitors["證券代號"]:
    time.sleep(random.randint(5, 20))
    #print(stockId)
    PE = GetPE(stockId)
    #print(PE)
    stock = twstock.Stock(stockId)
    print("current PE:" + PE['CurrentPE'])
    print("current price:" + stock.price[-1:][0])
    print("low PE:" + list(PE.values())[2])

    # 本益比 < 10, 目前股價小於最小級距本益比
    if Decimal(PE['CurrentPE']) < 10 and stock.price[-1:][0] < Decimal(list(PE.values())[2]):
        print("choose:" + stockId)