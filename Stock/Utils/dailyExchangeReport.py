import requests
import json
import pandas as pd
from functools import reduce


def GetDailyExchange():
    # 下載股價
    response = requests.get(
        'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json')
    # print(response.json());
    data = json.loads(response.text)
    # print(data["select_columns"])
    # print(data["data"])

    df = pd.DataFrame(data["data"], columns=data["fields"])
    # print(df)

    # 下載收盤價
    response = requests.get(
        "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&type=ALLBUT0999")
    data = json.loads(response.text)

    df2 = pd.DataFrame(data["data9"], columns=data["fields9"])
    # print(data["fields9"])
    # 合併漲跌價差跟符號欄位
    df2['漲跌'] = df2['漲跌(+/-)'].apply(lambda x: '+' if "green" in x else '-') + df2['漲跌價差']
    df2 = df2[["證券代號", "收盤價", "漲跌"]]
    #df2 = pd.concat(df2, keys=["漲跌(+/-)", "漲跌價差"])

    # print(df2)
    return reduce(lambda df1, df2: pd.merge(df1, df2, on='證券代號'), [df, df2])


#df = GetDailyExchange()
#print(df)

#print(merge[pd.DataFrame(df['證券名稱'].tolist()).isin(['根基', '冠德']).any(1).values])
# print(merge['證券代號'].to_csv(header=None, index=False).strip('\r\n').split('\r\n')) # 列印所有證券代號

'''
# 本益比(Price-to-Earning Ratio)
PE = pd.to_numeric(merge['本益比'], errors='coerce') < 15
DY = pd.to_numeric(merge['殖利率(%)'], errors='coerce') > 5  # 殖利率(Dividend yield)
# 淨價比(Price-to-Book Ratio) 找到股價淨值比小於0.7的股票
PBR = pd.to_numeric(merge['股價淨值比'], errors='coerce') <= 1.81
candidate = merge[(PE & DY & PBR)]
print(candidate)
'''