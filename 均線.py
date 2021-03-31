import requests
import json
import pandas as pd
import datetime
import calendar
import time
import numpy as np


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def GetDailyTradePrice(stockId):
    fields = list()
    data = list()
    df = object
    now = datetime.datetime.now()

    index = 0
    while len(data) <= 60:

        # 休息一下再抓, 避免存取過於頻繁被擋
        # time.sleep(np.random.randint({True: 0, False: 10}[index == 0], 30))
        date = add_months(now, -index).strftime("%Y%m%d")
        url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stockId}'
        # print(url)
        res = requests.get(url)
        res.encoding = "utf-8"
        # print(res.text)

        # 讀取json檔
        jsonData = json.loads(res.text)
        fields = jsonData["fields"]
        data.extend(jsonData["data"])
        # print(data)
        index += 1

    df = pd.DataFrame(data=data, columns=fields)
    # print(df)
    df['收盤價'] = df['收盤價'].astype(float)
    return df.sort_values(by='日期', ascending=False)[['日期', '收盤價']]  # 排序


def GetSma(df, day):
    return df['收盤價'][:day].sum() / day


df = GetDailyTradePrice('2330')
print(GetSma(df, 5))
print(GetSma(df, 20))
print(GetSma(df, 60))
#sma5 = df.收盤價.rolling(5).mean()
# print(df['收盤價'].rolling(5))
# print(sma5.head(5))
# combine long and short signals
# print(result)
