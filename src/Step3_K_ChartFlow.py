from io import StringIO
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import random
import time
import pyuser_agent
import time
import Utils

"""
抓取本益比
取得現今EPS、本益比、近五年六個級距本益比

選股條件：
1. 本益比小於10
2. 小於近五年最小級距本益比
"""


def GetPE(stockId):
    url = f"https://goodinfo.tw/tw/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stockId}&CHT_CAT=WEEK"
    css_selector = "#divK_ChartFlowDetail"
    try:
        list = Utils.GetDataFrameByCssSelector(url, css_selector)
        print(list)
        # 取前兩列後面倒數6欄資料, 轉成DataFrame
        firstRowDf = list.iloc[:1, -6:]
        print(firstRowDf)
    except:
        time.sleep(random.randint(20, 30))
        df = GetDataFrameByCssSelector(url, css_selector)

        # 取前兩列後面倒數6欄資料
        firstRowDf = list.iloc[:1, -6:]
        #print(firtRowDf)

    # dataframe轉成dictionary 參考 https://stackoverflow.com/questions/45452935/pandas-how-to-get-series-to-dict
    dictionaries = [
        dict(key=re.findall(r'[0-9]+[.]?[0-9]*', str(k))[0], value=v) 
        for k, v in firstRowDf.items()
    ]
   
    #print(dictionaries)

    # 轉換成dataframe
    data = []
    headers = [
        "本益比-級距1倍數",
        "本益比-級距1價格",
        "本益比-級距2倍數",
        "本益比-級距2價格",
        "本益比-級距3倍數",
        "本益比-級距3價格",
        "本益比-級距4倍數",
        "本益比-級距4價格",
        "本益比-級距5倍數",
        "本益比-級距5價格",
        "本益比-級距6倍數",
        "本益比-級距6價格",
    ]
    for entry in dictionaries:
        # print(entry)
        data.append(entry["key"])
        data.append(entry["value"])

    #print(headers)
    #print(data)
    df = pd.DataFrame([data], columns=headers)
    return df


# ------ 共用的 function ------
def GetDataFrameByCssSelector(url, css_selector):
    ua = pyuser_agent.UA()
    user_agent = ua.random
    headers = {"user-agent": user_agent}
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find(id=css_selector)
    print(data)
    try:
        #讀取網頁內容，並轉成pd.DataFrame
        dfs = pd.read_html(StringIO(data.prettify()), displayed_only=False)
    except:
        return pd.DataFrame()

        # Return the first DataFrame with more than one row
    for df in dfs:
        if len(df) > 1:
            return df

    # If no suitable DataFrame is found, return an empty DataFrame
    return pd.DataFrame()


# ------ 測試 ------

data = GetPE('2330')
print(data)

