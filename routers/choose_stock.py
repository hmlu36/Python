import pandas as pd
from datetime import datetime, timedelta, date
import time
from io import StringIO
from decimal import Decimal
import random
import json
import os
import pathlib

from src.Step0_InstitutionalInvestors import GetInstitutionalInvestorsExchange
from src.Step1_BasicStockInfo import GetBasicStockInfo
from src.Step2_FinDetail import GetFinDetail
from src.Step3_K_ChartFlow import GetPE
from src.Step4_K_Chart import GetTransaction
import src.Step5_ShareholderDistribution as shareholderDistribution
from src.Step6_StockDividendPolicy import GetDividend
from src.Step7_VolumeData import GetVolume
import src.Step8_DirectorSharehold as directorSharehold
import src.Step9_DailyTopVolume as dailyTopVolume
import requests
from fastapi import APIRouter
from typing import Union
from dotenv import load_dotenv

"""
選股條件：
（1）評估價值是否被低估？（股票價格不會太貴）
1. 本益比　　　< 15倍
2. 現金殖利率　> 5 %

（2）本益比低估
1. 本益比小於10
2. 小於近五年最小級距本益比

（3）確定本業利益是成長的，且為本業賺的（不是靠業外收益賺的，獲利不持久）
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10
"""

router = APIRouter(
    prefix="/choose_stock",
    tags=["choose_stock"],
    responses={404: {"description": "Not found"}},
)

stocks = [
    "1229",
    "1231",
    "1409",
    "1304",
    "1308",
    "1474",
    "1515",
    "1604",
    "2020",
    "2069",
    "2324",
    "2347",
    "2352",
    "2385",
    "2387",
    "2417",
    "2458",
    "2488",
    "2520",
    "2546",
    "2881",
    "3005",
    "3028",
    "3033",
    "3044",
    "3048",
    "3209",
    "3231",
    "3312",
    "3702",
    "3706",
    "6257",
    "8112",
    "8150",
]


@router.get("/operate/{op}")
def Operate(op: int, stockId: Union[str, None] = None):
    # 三大法人買賣金額統計表
    if op == 0:
        return GetInstitutionalInvestorsExchange()
        
    # 過濾清單
    if op == 1:
        df = GetBasicStockInfo(True)
        # print(df)

        df.update(df.apply(lambda x: pd.to_numeric(x, errors="coerce")))

        cond1 = df["毛利率"] > 30
        cond2 = df["營業利益率"] > 30
        cond3 = df["本益比"] < 15
        cond3 = df["資本額"] > 15
        df = df[cond1 & cond2 & cond3]
        # print(df)

        tableName = "過濾清單"
        # 清除所有資料
        deleteAll(tableName)

        # 重新寫入
        save(tableName, df)
        return {"message": "執行成功"}

    # 明細資料
    if op == 2:
        basicStockInfo_df = GetBasicStockInfo()
        print(stockId)

        stockInfo_df = basicStockInfo_df[basicStockInfo_df["證券代號"] == stockId]
        stockInfo_df.reset_index(drop=True, inplace=True)
        print(stockInfo_df)

        if not stockInfo_df.empty:
            Sleep()
            finDetail_df = GetFinDetail(stockId)
            print(finDetail_df)

            PE_df = GetPE(stockId)
            print(PE_df)

            Sleep()
            transaction_df = GetTransaction(stockId)
            print(transaction_df)

            volume_df = GetVolume(stockId)
            print(volume_df)

            Sleep()
            dividend_df = GetDividend(stockId)
            print(dividend_df)

            Sleep()
            distribution_df = shareholderDistribution.GetDistribution(stockId)
            print(distribution_df)

            # 合併所有欄位成一列
            temp_df = pd.concat([stockInfo_df, transaction_df, volume_df, PE_df, distribution_df, finDetail_df, dividend_df], axis=1)
            print(temp_df)

            # 將列合併入dataframe
            # sum_df = pd.concat([sum_df, temp_df], axis=0)

            response = retrieve("彙整清單", "證券代號", stockId)
            records = json.loads(response.text)["records"]
            if len(records) == 0:
                save("彙整清單", temp_df)
            else:
                updateJsonData = {"records": [{"id": records[0]["id"], "fields": jsonData["records"][0]["fields"]}]}
                print(updateJsonData)
                updateJson("彙整清單", updateJsonData)

        return {"message": "執行成功"}

    # 日常籌碼面資料
    if op == 3:
        basicStockInfo_df = GetBasicStockInfo()
        # sum_df = pd.DataFrame()
        for stockId in stocks:
            print(stockId)

            stockInfo_df = basicStockInfo_df[basicStockInfo_df["證券代號"] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)

            if not stockInfo_df.empty:
                Sleep()
                transaction_df = GetTransaction(stockId)
                print(transaction_df)

                volume_df = GetVolume(stockId)
                print(volume_df)

                temp_df = pd.concat([stockInfo_df, transaction_df, volume_df], axis=1)
                print(temp_df)

                temp_df.to_csv(f"\Data\Daily\籌碼面資料.csv", mode="a", header=False, encoding="utf_8_sig")
                # 合併所有欄位成一列
                # sum_df = pd.concat([sum_df, temp_df], axis=0)

        # 將列合併入dataframe
        # sum_df.to_csv('籌碼面資料.csv',encoding='utf_8_sig')

    # 大戶、本益比
    if op == 4:
        shareholderDistribution.WriteData()

        for stockId in stocks:
            print(stockId)

            Sleep()
            distribution_df = shareholderDistribution.GetDistribution(stockId)
            print(distribution_df)

            Sleep()
            PE_df = GetPE(stockId)
            print(PE_df)

            temp_df = pd.concat([PE_df, distribution_df], axis=1)
            print(temp_df)

            temp_df.to_csv(f'\Data\\Weekly\股東分布_本益比_{date.today().strftime("%Y%m%d")}.csv', mode="a", header=False, encoding="utf_8_sig")

    if op == 5:
        directorSharehold.WriteData()

    if op == 7:
        basicStockInfo_df = GetBasicStockInfo()
        topVolumeStocks = dailyTopVolume.GetTopVolume()[:100]

        for stockId in topVolumeStocks:
            print(stockId)

            stockInfo_df = basicStockInfo_df[basicStockInfo_df["證券代號"] == stockId]
            stockInfo_df.reset_index(drop=True, inplace=True)
            print(stockInfo_df)

            if not stockInfo_df.empty:
                volume_df = GetVolume(stockId)
                print(volume_df)

                temp_df = pd.concat([stockInfo_df, volume_df], axis=1)
                print(temp_df)

                temp_df.to_csv(f'\Data\Daily\異常籌碼資料_{date.today().strftime("%Y%m%d")}.csv', mode="a", header=False, encoding="utf_8_sig")

        # 刪除暫存檔案
        try:
            folderPath = pathlib.Path(f'\Data\Daily\Chip\{(date.today() - timedelta(days=1)).strftime("%Y%m%d")}')
            delete_folder(folderPath)
        except Exception as ex:
            print(ex)

    if op == 999:
        jsonData = {
            "records": [
                {
                    "fields": {
                        "2018": "  2.58 /    0.0",
                        "2019": "   5.0 /    0.0",
                        "2020": "   6.5 /   0.0",
                        "2021": "   9.0 /    0.0",
                        "2022": " 13.81 /    0.0",
                        "證券代號": "2458",
                        "證券名稱": "義隆",
                        "公司名稱": "義隆電子股份有限公司",
                        "資本額": 30.38803968,
                        "成立日期": "19940505",
                        "上市日期": "20010917",
                        "殖利率": "12.85",
                        "本益比": "6.37",
                        "淨值比": "2.66",
                        "收盤(1ma / 5ma / 20ma / 60ma)": "👎   107.5 /    108.3 /   108.55 /   131.06",
                        "張數(1ma / 5ma / 20ma / 60ma)": "   975.0 /   1167.2 /  1797.75 /  1372.68",
                        "外資持股(%)(1ma / 5ma / 20ma / 60ma)": "    23.5 /    23.38 /    22.86 /     22.0",
                        "券資比(%)(1ma / 5ma / 20ma / 60ma)": "    33.1 /    26.14 /    15.24 /     9.47",
                        "超額買超": 0.98,
                        "重押券商": "",
                        "前15卷商籌碼集中度": "0.06",
                        "買賣家數差": 78,
                        "本益比-級距1倍數": "9",
                        "本益比-級距1價格": "152.1",
                        "本益比-級距2倍數": "11",
                        "本益比-級距2價格": "185.9",
                        "本益比-級距3倍數": "13",
                        "本益比-級距3價格": "219.7",
                        "本益比-級距4倍數": "15",
                        "本益比-級距4價格": "253.5",
                        "本益比-級距5倍數": "17",
                        "本益比-級距5價格": "287.3",
                        "本益比-級距6倍數": "19",
                        "本益比-級距6價格": "321.1",
                        "100張以下比例": "36.17  /  35.72  /  35.5  /  35.8  /  35.44",
                        "100-1000張比例": "16.11  /  16.55  /  16.24  /  16.71  /  17.22",
                        "1000張以上比例": "47.66  /  47.63  /  48.17  /  47.61  /  47.25",
                        "1000張以上人數": "45.0  /  45.0  /  46.0  /  46.0  /  45.0",
                        "毛利率": "47.24",
                        "營業利益率": "27.15",
                        "ROE": "27.02",
                        "稅前淨利率": "24.72",
                        "稅後淨利率": "18.86",
                        "總資產週轉率": "0.93",
                        "本業收益": "109.83",
                        "每股營業現金流量": "2.66",
                        "每股自由現金流量": "-1.5",
                        "財報評分": "68",
                    }
                }
            ]
        }
        response = retrieve("彙整清單", "證券代號", "2458")
        records = json.loads(response.text)["records"]
        print(records)
        if len(records) == 0:
            createJson("彙整清單", jsonData)
        else:
            newJsonData = {"records": [{"id": records[0]["id"], "fields": jsonData["records"][0]["fields"]}]}
            print(newJsonData)
            updateJson("彙整清單", newJsonData)


# ------ 共用的 function ------


def delete_folder(path):
    for sub in path.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    path.rmdir()


load_dotenv()
BASE_ID = os.environ.get("BASE_ID")
API_KEY = os.environ.get("API_KEY")

# Headers
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json; charset=utf-8"}
url = f"https://api.airtable.com/v0/{BASE_ID}/"


def createJson(tableName, data):
    response = requests.post(url + tableName, data=json.dumps(data), headers=headers)
    print(response.json())


def updateJson(tableName, data):
    response = requests.patch(url + tableName, data=json.dumps(data), headers=headers)
    print(response.json())


def save(tableName, df):
    # 每次上限為10筆
    if len(df.index) > 10:
        pageSize = 10
        totalItems = df.shape[0] 
        totalPages = totalItems // pageSize
        startIndex = 0
        endIndex = 0
        print("dataframe page size:" + str(totalPages))
        for pageIndex in range(totalPages + 1):
            print('pageIndex:' + str(pageIndex))
            startIndex = pageSize * pageIndex
            endIndex = pageSize * (pageIndex + 1) - 1
            if endIndex > totalItems:
                endIndex = totalItems
            print("start:" + str(startIndex) + ", end:" + str(endIndex))
            print(df.iloc[startIndex : endIndex])
            jsonData = dataFrame2Json(df.iloc[startIndex : endIndex])
            createJson(tableName, jsonData)
    else:
        jsonData = dataFrame2Json(df)
        createJson(tableName, jsonData)

# 刪除上限為10筆
def deleteAll(tableName):
    response = getAll(tableName)
    allRecords = json.loads(response.text)
    # print(allRecords)
    deleteParams = ""
    count = 0
    for record in allRecords["records"]:
        deleteParams = deleteParams + ("&" if deleteParams != "" else "") + "records[]=" + record["id"]
        count += 1
        if (count % 10 == 0) or (count == len(allRecords["records"])):
            # print(deleteParams)
            tempUrl = url + tableName + ("?" if deleteParams != "" else "") + deleteParams
            requests.delete(tempUrl, headers=headers)
            deleteParams = ""


def getAll(tableName):
    return requests.get(url + tableName, headers=headers)


def retrieve(tableName, column, value):
    tempUrl = url + tableName + "?filterByFormula={" + column + "}='" + value + "'"
    print(tempUrl)
    return requests.get(tempUrl, headers=headers)


def dataFrame2Json(df):
    """
    格式必須為
    {
        "records" [
            {
                "fields": {
                    "Column1": value
                }
            },
            {
                "fields": {
                    "Column1": value
                }
            },
            ...
        ]
    }
    """
    pd_json = df.to_json(orient="records")
    jsonRecord = json.loads(pd_json)

    fields = []
    for record in jsonRecord:
        for k, v in record.items():
            try:
                # 轉為文字
                if k in (
                    "證券代號",
                    "成立日期",
                    "上市日期",
                    "收盤(1ma / 5ma / 20ma / 60ma)",
                    "張數(1ma / 5ma / 20ma / 60ma)",
                    "外資持股(%)(1ma / 5ma / 20ma / 60ma)",
                    "券資比(%)(1ma / 5ma / 20ma / 60ma)",
                    "重押券商",
                    """
                    "100張以下比例",
                    "100-1000張比例",
                    "1000張以上比例",
                    "1000張以上人數",
                    """,
                ):
                    record[k] = str(v)
                else:
                    record[k] = v
            except (ValueError, TypeError):
                pass
        entry = {"fields": record}
        fields.append(entry)

    data = {"records": fields}
    print(data)
    return data


def Sleep():
    time.sleep(random.randint(10, 20))


# ------ 測試 ------
# 0 產生過濾清單(本益比、殖利率、淨值比、收盤價、全體董監持股、股東分布人數)
# 1 產生過濾清單(同0含本益比)
# 2 抓出股票明細資料
# 3 日排程 - 籌碼面資料
# 4 週排程 - 大戶、本益比
# 5 月排程 - 董監比例
# 6 季排程 - 財務資料
# 7 日排程 - 異常買入
# GetChampionStock(0)
