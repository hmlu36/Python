from matplotlib.font_manager import json_load
import pandas as pd
import requests
from datetime import datetime
from decimal import Decimal

# 取出每日收盤價
def GetDailyExchange():
    now = datetime.now()
    url = f'https://www.twse.com.tw/fund/BFI82U?response=json&dayDate={now.strftime("%Y%m%d")}&type=day'
    #print(url)
    response = requests.get(url)
    jsonData = response.json()
    #print(jsonData)
    #print(jsonData["data"])
    #print(jsonData["fields"])
    df = pd.DataFrame(jsonData["data"], columns=jsonData["fields"])
    df["買賣差額"] = (pd.to_numeric(df["買賣差額"].str.strip().str.replace(",", ""))  / 100000000).round(3)
    df = df[['單位名稱', '買賣差額']]
    return df


# ------ 測試 ------
'''
print(GetDailyExchange())
'''