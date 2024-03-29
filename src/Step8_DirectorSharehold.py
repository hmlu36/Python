from io import StringIO
from bs4 import BeautifulSoup
import requests
import random
import time
import pandas as pd
import os
import pyuser_agent


def GetStockBoardTop():
    # 取自神秘金字塔
    url = "https://norway.twsthr.info/StockBoardTop.aspx"
    cssSelector = "#details"
    df = GetDataFrameByCssSelector(url, cssSelector)
    df.columns = df.columns.get_level_values(0)
    df = df.iloc[:, [3, 7]]
    
    df['證券代號'] = df['個股代號/名稱'].str[0:4]
    df['公司名稱'] = df['個股代號/名稱'].str[4:]
    df = df[['證券代號', '公司名稱', '持股比率 %']]
    df = df.rename(columns={"持股比率 %": "全體董監持股(%)"})
    #df.to_csv(f"{GetRootPath()}\Data\Monthly\董監持股比例.csv", encoding="utf_8_sig")
    return df


def GetDirectorSharehold():
    cssSelector = "#divStockList"
    sum_df = pd.DataFrame()

    for rankIndex in range(0, 5):
        url = f"https://goodinfo.tw/tw/StockList.asp?SHEET=董監持股&MARKET_CAT=熱門排行&INDUSTRY_CAT=全體董監持股比例&RANK={str(rankIndex)}"
        print(url)

        try:
            time.sleep(random.randint(5, 10))
            df = GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            sum_df = pd.concat([sum_df, df], axis=0)
            # df.columns = df.columns.get_level_values(1)
        except:
            time.sleep(random.randint(20, 30))
            df = GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            # df.columns = df.columns.get_level_values(1)

    # 去除重複標頭
    sum_df = sum_df[~(sum_df == sum_df.columns).all(axis=1)]
    # sum_df.to_csv(f'{GetRootPath()}\Data\Monthly\董監持股比例.csv',encoding='utf_8_sig')
    return sum_df


# ------ 共用的 function ------
def GetDataFrameByCssSelector(url, css_selector):
    ua = pyuser_agent.UA()
    user_agent = ua.random
    headers = {"user-agent": user_agent}
    rawData = requests.get(url, headers=headers)
    rawData.encoding = "utf-8"
    soup = BeautifulSoup(rawData.text, "html.parser")
    data = soup.select_one(css_selector)
    try:
        dfs = pd.read_html(StringIO(data.prettify()))
    except:
        return pd.DataFrame()

    # print(dfs)
    if len(dfs[0]) > 1:
        return dfs[0]
    if len(dfs[1]) > 1:
        return dfs[1]
    return dfs


def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------ 測試 ------
print(GetDirectorSharehold())
#print(GetStockBoardTop())
