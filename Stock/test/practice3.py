
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import random
import html5lib

# ----------------- （１）評估價值是否被低估？（股票價格不會太貴） -------------
########## 去公開資訊觀測站，把本益比、股價淨值比爬下來 ##########
url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_=' + \
    str(time.time())
list_req = requests.get(url)
soup = BeautifulSoup(list_req.content, "html.parser")
getjson = json.loads(soup.text)

# 因為是表格式，用dataframe處理會比較方便
stockdf = pd.DataFrame(getjson['data'], columns=[
                       "證券代號", "證券名稱", "殖利率(%)", "股利年度", "本益比", "股價淨值比", "財報年/季"])
PBR = pd.to_numeric(stockdf['股價淨值比'], errors='coerce') < 1  # 找到股價淨值比小於0.7的股票
PER = pd.to_numeric(stockdf['本益比'], errors='coerce') > 5  # 找到本益比小於15的股票
DividendYield = pd.to_numeric(stockdf['殖利率(%)'].replace(
    '-', 0), errors='coerce') > 5  # 殖利率 > 5

candidate = stockdf[(PBR & PER & DividendYield)]  # 綜合以上兩者，選出兩者皆符合的股票
print(candidate)
