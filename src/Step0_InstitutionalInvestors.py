import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import *
import time
import random


def GetDailyExchangeData(dayCount=1):
    iie_df = GetInstitutionalInvestorsExchange(dayCount)
    dea_df = GetDailyExchangeAmount(dayCount)
    sum_df = pd.concat([iie_df, dea_df])
    sum_df.loc['三大法人比例'] = ((sum_df.iloc[0:4].abs().sum(axis=0, numeric_only=True) / sum_df.loc['總成交金額']) * 100).round(3)
    print(sum_df)


# 取出每日收盤價
# 計算60個交易日
def GetInstitutionalInvestorsExchange(dayCount=1):
    count = 0
    sum_df = pd.DataFrame()
    while sum_df.shape[1] < dayCount + 1:
        tempDate = datetime.today() - pd.tseries.offsets.BDay(count)
        print(tempDate)
        url = f"https://www.twse.com.tw/fund/BFI82U?response=json&dayDate={tempDate.strftime('%Y%m%d')}&type=day"
        # print(url)
        response = requests.get(url)
        jsonData = response.json()
        # print(jsonData)
        # print(jsonData["data"])
        # print(jsonData["fields"])
        if jsonData["stat"] == "OK":
            df = pd.DataFrame(jsonData["data"], columns=jsonData["fields"])
            df["買賣差額"] = (pd.to_numeric(df["買賣差額"].str.strip().str.replace(",", "")) / 100000000).round(3)
            df = df[["單位名稱", "買賣差額"]]
            df = df.rename(columns={"買賣差額": str(tempDate.year - 1911) + "/" + tempDate.strftime("%m/%d")})
            # print(df)

            if sum_df.empty:
                sum_df = df
            else:
                sum_df = pd.merge(sum_df, df, on=["單位名稱"])

        print(sum_df)
        count += 1
        #Sleep()

    sum_df = sum_df.set_index("單位名稱")
    print(sum_df)
    return sum_df


# ------ 共用的 function ------
def GetDailyExchangeAmount(dayCount=1):
    count = 0
    sum_df = pd.DataFrame()
    # print(tempDate + relativedelta(months=-6))

    while sum_df.shape[1] < dayCount + 1:
        tempDate = datetime.today() - relativedelta(months=count)
        url = f"https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date={tempDate.strftime('%Y%m%d')}"

        response = requests.get(url)
        jsonData = response.json()
        print(jsonData)

        df = pd.DataFrame(jsonData["data"], columns=jsonData["fields"])
        df = df[["日期", "成交金額"]]
        df["成交金額"] = (pd.to_numeric(df["成交金額"].str.strip().str.replace(",", "")) / 100000000).round(3)
        df = df.rename(columns={"成交金額": "總成交金額"})
        print(df)

        df = df.set_index("日期").T
        print(df)

        if sum_df.empty:
            sum_df = df
        else:
            sum_df = pd.merge(sum_df, df, on=["日期"])
            # sum_df = pd.concat([sum_df, df], axis = 1)

        count += 1
        print(sum_df)
        #Sleep()

    sum_df = sum_df.sort_values(by="日期", axis=1, ascending=False)

    print(sum_df)
    print(sum_df.shape[1])
    return sum_df.iloc[:, 0: dayCount]


def Sleep():
    time.sleep(random.randint(3, 10))


# ------ 測試 ------
# GetInstitutionalInvestorsExchange()
#GetDailyExchangeAmount()
GetDailyExchangeData()
