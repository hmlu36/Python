from bs4 import BeautifulSoup
import pandas as pd
import os
import pyuser_agent
from requests import Session
import ssl
import urllib.request
from io import StringIO
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time


def GetAllShareholderDistribution():
    url = "https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5"

    context = ssl._create_unverified_context()

    # 使用這個 context 來打開連線
    with urllib.request.urlopen(url, context=context) as response:
        df = pd.read_csv(response)

    # 列轉成欄位
    # 參考 https://stackoverflow.com/questions/63413708/transforming-pandas-dataframe-convert-some-row-values-to-columns
    df["key2"] = df.groupby("證券代號").cumcount() + 1
    s = (
        df.set_index(["資料日期", "證券代號", "key2"])
        .unstack()
        .sort_index(level=1, axis=1)
    )
    s.columns = s.columns.map("{0[0]}_{0[1]}".format)
    s = s.rename_axis([None], axis=1).reset_index()
    # s.to_csv('股東分布資料.csv',encoding='utf_8_sig')
    # print(s)

    retailHeaders = [
        "1-999",
        "1,000-5,000",
        "5,001-10,000",
        "10,001-15,000",
        "15,001-20,000",
        "20,001-30,000",
        "30,001-40,000",
        "40,001-50,000",
        "50,001-100,000",
    ]
    distributionRangeHeaders = retailHeaders + [
        "100,001-200,000",
        "200,001-400,000",
        "400,001-600,000",
        "600,001-800,000",
        "800,001-1,000,000",
        "1,000,001",
        "差異數調整",
        "合計",
    ]

    newTitle = ["資料日期", "證券代號"] + [
        distribution + title
        for distribution in distributionRangeHeaders
        for title in ["人數", "比例", "持股分級", "股數"]
    ]
    # print(newTitle)
    s.columns = newTitle

    # print(s)
    s["100張以下比例"] = s[
        [retailHeader + title for retailHeader in retailHeaders for title in ["比例"]]
    ].sum(axis=1)
    s["100張以下人數"] = s[
        [retailHeader + title for retailHeader in retailHeaders for title in ["人數"]]
    ].sum(axis=1)
    s = s.rename(
        columns={
            "100,001-200,000比例": "101-200張比例",
            "100,001-200,000人數": "101-200張人數",
            "200,001-400,000比例": "201-400張比例",
            "200,001-400,000人數": "201-400張人數",
            "400,001-600,000比例": "401-600張比例",
            "400,001-600,000人數": "401-600張人數",
            "600,001-800,000比例": "601-800張比例",
            "600,001-800,000人數": "601-800張人數",
            "800,001-1,000,000比例": "801-1000張比例",
            "800,001-1,000,000人數": "801-1000張人數",
            "1,000,001比例": "1000張以上比例",
            "1,000,001人數": "1000張以上人數",
        }
    )
    s["401-800張人數"] = s[["401-600張人數", "601-800張人數"]].sum(axis=1)
    s["401-800張比例"] = s[["401-600張比例", "601-800張比例"]].sum(axis=1)
    # print(s.columns)
    s = s[
        [
            "證券代號",
            "100張以下人數",
            "100張以下比例",
            "101-200張人數",
            "101-200張比例",
            "201-400張人數",
            "201-400張比例",
            "401-800張人數",
            "401-800張比例",
            "801-1000張人數",
            "801-1000張比例",
            "1000張以上人數",
            "1000張以上比例",
        ]
    ]

    print(s)
    # s.to_csv(f'{GetRootPath()}\Data\Weekly\股東分布資料.csv',encoding='utf_8_sig')
    return s


def GetShareholderDistribution(stockId):
    url = "https://www.tdcc.com.tw/portal/zh/smWeb/qryStock"

    ua = pyuser_agent.UA()
    user_agent = ua.random
    headers = {"user-agent": user_agent}

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url, headers=headers)
    print(session.cookies.get_dict())
    soup = BeautifulSoup(response.text, "html.parser")

    select = soup.find("select", {"id": "scaDate"})
    options = [option.text for option in select.find_all("option")]
    lastDate = options[0]

    # 找到名為 'SYNCHRONIZER_TOKEN' 的 <input> 元素
    synchronizer_token = soup.find("input", {"name": "SYNCHRONIZER_TOKEN"})["value"]
    # print(synchronizer_token)

    # 找到名為 'SYNCHRONIZER_URI' 的 <input> 元素
    synchronizer_uri = soup.find("input", {"name": "SYNCHRONIZER_URI"})["value"]
    # print(synchronizer_uri)

    # print('date:' + date)
    payload = {
        "SYNCHRONIZER_TOKEN": synchronizer_token,
        "SYNCHRONIZER_URI": synchronizer_uri,
        "method": "submit",
        "firDate": lastDate,
        "scaDate": lastDate,
        "sqlMethod": "StockNo",
        "stockNo:": f"{stockId}",
        "stockName": "",
    }

    print(headers)
    print(payload)

    cookies_dict = {}
    for cookie in session.cookies:
        if cookie.name not in cookies_dict:
            cookies_dict[cookie.name] = []
        cookies_dict[cookie.name].append(cookie.value)
    print(cookies_dict)

    time.sleep(1)
    rawData = session.post(url, data=payload, headers=headers)
    # print(rawData.text)
    soup = BeautifulSoup(rawData.text, "html.parser")
    # print(soup)
    # 取出<table class="table">的內容
    table = soup.find("table", {"class": "table"})
    # print(table)

    # 把table轉成DataFrame

    table_str = table.prettify()
    df = pd.read_html(StringIO(table_str))[0]
    print(df)


def GetShareholderDistribution2(stockId):
    url = "https://www.tdcc.com.tw/portal/zh/smWeb/qryStock"

    # 創建一個新的 Chrome 瀏覽器實例
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service)

    # 讓瀏覽器打開指定的網址
    driver.get(url)

    # 獲取網頁的 HTML 內容
    html = driver.page_source

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    select = soup.find("select", {"id": "scaDate"})
    options = [option.text for option in select.find_all("option")]
    lastDate = options[0]

    # 找到名為 'SYNCHRONIZER_TOKEN' 的 <input> 元素
    synchronizer_token = soup.find("input", {"name": "SYNCHRONIZER_TOKEN"})["value"]

    # 找到名為 'SYNCHRONIZER_URI' 的 <input> 元素
    synchronizer_uri = soup.find("input", {"name": "SYNCHRONIZER_URI"})["value"]

    # 填充表單並提交
    select = Select(driver.find_element(By.ID, "scaDate"))
    select.select_by_visible_text(lastDate)
    driver.find_element(By.NAME, "stockNo").send_keys(stockId)
    #driver.find_element(By.NAME, "method").click()

    # 等待結果頁面加載
    time.sleep(5)

    # 獲取結果頁面的 HTML 內容
    result_html = driver.page_source

    # 使用 BeautifulSoup 解析結果頁面的 HTML
    result_soup = BeautifulSoup(result_html, "html.parser")

    # 取出<table class="table">的內容
    table = result_soup.find("table", {"class": "table"})

    # 把table轉成DataFrame
    table_str = table.prettify()
    df = pd.read_html(StringIO(table_str))[0]
    print(df)

    # 關閉瀏覽器
    #driver.quit()


# ------ 共用的 function ------
def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 總表
# WriteData()


# ------ 測試 ------

# 個股(含歷程)
df = GetShareholderDistribution2(2330)
print(df)

# print(GetAllShareholderDistribution())
