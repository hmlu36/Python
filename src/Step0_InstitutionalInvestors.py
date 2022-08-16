import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import *
import time
import random
from fake_useragent import UserAgent

# 取出每日收盤價
# 計算n個交易日
def GetInstitutionalInvestorsExchange(dayCount=1):
    amount_df = GetDailyExchangeAmount(dayCount)

    count = 0
    sum_df = pd.DataFrame()
    while sum_df.shape[1] < dayCount + 1:
        tempDate = datetime.today() - pd.tseries.offsets.BDay(count)
        mingoDateStr = str(tempDate.year - 1911) + "/" + tempDate.strftime("%m/%d")
        # print(tempDate)
        url = f"https://www.twse.com.tw/fund/BFI82U?response=json&dayDate={tempDate.strftime('%Y%m%d')}&type=day"
        # print(url)

        response = requests.get(url, headers=GetHeaders())
        jsonData = response.json()
        # print(jsonData)

        if jsonData["stat"] == "OK":
            df = pd.DataFrame(jsonData["data"], columns=jsonData["fields"])
            df["買賣差額"] = pd.to_numeric(df["買賣差額"].str.strip().str.replace(",", ""))
            # print(df)
            total = (int(df.loc[5, "買進金額"].replace(",", "")) + int(df.loc[5, "賣出金額"].replace(",", ""))) / 2
            # print(total)
            # print((amount_df.loc["總成交金額", mingoDateStr]))
            df = df[["單位名稱", "買賣差額"]]
            #print(df)

            # 新增列 (市場總交易金額)
            temp_df = pd.DataFrame([{"單位名稱": "市場總交易金額", "買賣差額": amount_df.loc["總成交金額", mingoDateStr]}])
            df = pd.concat([df, temp_df], axis=0, ignore_index=True)

            # 單位轉為億, 取小數點第三位
            df["買賣差額"] = (pd.to_numeric(df["買賣差額"], downcast="float") / 100000000).round(3)

            # 新增列 (法人成交比重)
            temp_df = pd.DataFrame([{"單位名稱": "法人成交比重", "買賣差額": (total / amount_df.loc["總成交金額", mingoDateStr] * 100).round(2)}])
            df = pd.concat([df, temp_df], axis=0, ignore_index=True)

            # 買賣差額 名稱改為名國年
            df = df.rename(columns={"單位名稱": "項目", "買賣差額": mingoDateStr})
            # print(df)

            if sum_df.empty:
                sum_df = df
            else:
                sum_df = pd.merge(sum_df, df, on=["項目"])

        # print(sum_df)
        count += 1
        Sleep()

    sum_df = sum_df.set_index("項目")
    print(sum_df)
    return sum_df


# 取得當日總成交金額
def GetDailyExchangeAmount(dayCount=1):
    count = 0
    sum_df = pd.DataFrame()
    # print(tempDate + relativedelta(months=-6))

    while sum_df.shape[1] < dayCount + 1:
        tempDate = datetime.today() - relativedelta(months=count)
        url = f"https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date={tempDate.strftime('%Y%m%d')}"

        response = requests.get(url, headers=GetHeaders())
        jsonData = response.json()
        # print(jsonData)

        df = pd.DataFrame(jsonData["data"], columns=jsonData["fields"])
        df = df[["日期", "成交金額"]]
        df["成交金額"] = pd.to_numeric(df["成交金額"].str.strip().str.replace(",", ""))
        df = df.rename(columns={"成交金額": "總成交金額"})
        # print(df)

        df = df.set_index("日期").T
        # print(df)

        if sum_df.empty:
            sum_df = df
        else:
            sum_df = pd.concat([sum_df, df], axis=1)

        count += 1
        # print(sum_df)
        Sleep()

    sum_df = sum_df.sort_values(by="日期", axis=1, ascending=False)

    print(sum_df)
    # print(sum_df.shape[1])
    return sum_df.iloc[:, 0:dayCount]


# ------ 共用的 function ------
def GetHeaders():
    ua = UserAgent()
    user_agent = ua.random
    headers = {"user-agent": user_agent}
    return headers


def Sleep():
    time.sleep(random.randint(3, 10))


# ------ 測試 ------
# GetInstitutionalInvestorsExchange()
# GetDailyExchangeAmount()
