from io import StringIO
import pandas as pd
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
import time
import random
import pyuser_agent

"""
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10 %
8. 董監持股比例 > 20
"""


def GetFinHeaders():
    return ["毛利率", "營業利益率", "股東權益報酬率  (年預估)", "稅前淨利率", "稅後淨利率", "總資產週轉率", "本業收益", "每股營業現金流量", "每股自由現金流量", "財報評分"]


def GetFinData(stockId):
    url = f"https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stockId}"
    css_selector = "#txtFinBody"
    try:
        df = GetDataFrameByCssSelector(url, css_selector)
    except:
        time.sleep(random.randint(20, 30))
        df = GetDataFrameByCssSelector(url, css_selector)
    # print(df)
    return df


def GetFinDetail(stockId):
    df = GetFinData(stockId)
    dict = {}

    headers = GetFinHeaders()
    for header in headers:
        if header == "本業收益":
            try:
                # 本業收益（營業利益率／稅前淨利率） > ６０％
                tempDict = round(Decimal(dict["營業利益率"]) / Decimal(dict["稅前淨利率"]) * 100, 2)
                dict.update({"本業收益": str(tempDict)})
            except:
                dict.update({"本業收益": "0"})
        else:
            try:
                # print(header)
                tempDict = GetDataFrameValueByLabel(df, "獲利能力", header)
                dict.update({header.replace("股東權益報酬率  (年預估)", "ROE"): str(Decimal(tempDict[0]))})
            except:
                dict.update({header.replace("股東權益報酬率  (年預估)", "ROE"): "0"})

    df = pd.DataFrame([dict])

    return df


"""
盈餘再投資比率

公式：
當季長期投資和固定資產 - 4年前同期長期投資和固定資產 / 近16季稅後淨利總和

盈餘再投資比率代表：
企業近4年來在長期投資、固定資產的增加幅度，相對於近4年獲利總和大小。 
由於長期投資、固定資產的投資金額龐大，如果企業自身獲利不足以支應， 
則資金上將出現龐大缺口，財務壓力上升。 
因此盈餘再投資比率過高，則代表企業的投資金額遠高於自身獲利能力，財務和周轉風險上升。 
此比率為洪瑞泰在其著作"巴菲特選股魔法書"中所創，書中建議低於80%財務較為穩健；高於200%則企業財務風險過高，投資人應避開。
"""


def GetBonusReinvestmentRate(stockId):
    df = GetFinData(stockId)


"""
def GetFinDetail2():
    url = "https://mops.twse.com.tw/mops/web/ajax_t163sb05"
    df = Utils.GetFromMops(url)
    print(df)
"""

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


# 取得dataframe比對相等(含有字元), 第一欄值
def GetDataFrameValueByLabel(df, columnLable, matchRowLable):
    return df.set_index(columnLable).filter(like=matchRowLable, axis=0).values[0]


# ------ 測試 ------
'''
data = GetFinDetail("8150")
print(data)
'''
"""
GetFinDetail2()
"""
