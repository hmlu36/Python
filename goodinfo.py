from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import sqlite3

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


# 抓取表格資料, 顯示出來
def GetGridData(stockId, cssSelector, titleIndex, topRecord):
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID="
    res = requests.get(url + stockId, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.select_one(cssSelector)
    # 標題
    columns = [td.text.replace('\n', '')
               for td in table.find_all('tr')[titleIndex].find_all('td')]
    # print(columns)

    # 內容
    rows = list()
    # 抓取第4筆以後的資料, 取前10筆
    for tr in table.find_all('tr')[(titleIndex + 1):][:topRecord]:
        rows.append([td.text.replace('\n', '').replace('\xa0', '')
                    for td in tr.find_all('td')])
        # print(rows)

    #df = pd.DataFrame(data=rows, columns=columns)
    # print(df)
    return rows


# 抓取個股股利
def GetStockDividend(stockId):
    GetGridData(stockId, '#FINANCE_DIVIDEND', 3, 10)
    # print(table)


# 抓取個股ROE、毛利等、EPS 等..明細
def GetStockDetail(stockId):
    return GetGridData(
        stockId, '#FINANCE_INCOME_M > div:nth-child(2) > div:nth-child(1) > table', 0, 10)


def GetDailyTradePrice(stockId):
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=${date}&stockNo="
    res = requests.get(url + stockId, headers=headers)
    res.encoding = "utf-8"
    # print(res.text)

    # 讀取json檔
    data = json.loads(res.text)
    columns = data["fields"]
    # print(columns)

    df = pd.DataFrame(data=data["data"], columns=columns)
    print(df)


# GetStockDividend("2330")
# GetStockDividend("2546")
# GetStockDetail("2546")


# GetDailyTradePrice("4414")

def GetConnection():
    return sqlite3.connect('stock.db')


def ExecuteSql(sql, args):
    try:
        con = GetConnection()

        # Execute the sql query
        con.execute(sql, args)

        # if sql.startswith('select') or sql.startswith('Select'):
        # Commit the data
        con.commit()

        print('Execute Sql Successfully')
    except Exception as e:
        print('Execute Sql worng, please check' + e)

    finally:
        # Close the connection
        con.close()


stockDetails = GetStockDetail("2546")
for detail in stockDetails:
    print(list(detail))
    ExecuteSql("Insert Into StockDetail(YearSeason, Revenue, ProfitAfterTax, GrossMargin, OperatingIncome, ProfitAfterTaxPercentage, ROE, EPS) values(?, ?, ?, ?, ?, ?, ?, ?)", list(detail))
