
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
2. 小於近五年本益比第1項
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}


        
competitors = GetCompetitor()
print(competitors)
for stockId in competitors["證券代號"]:
    print(stockId)
    PE = GetPE(stockId)
    print(PE)
    print(list(PE.values())[2])
    stock = twstock.Stock(stockId)
    print(stock.price[-1:][0])
    if Decimal(PE['PE_now']) < 10 & stock.price[-1:][0] < Decimal(list(PE.values())[2]):
        print("choose:" + stockId)