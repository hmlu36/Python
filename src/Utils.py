import re
from datetime import datetime, date
import pandas as pd
from bs4 import BeautifulSoup
import requests
from BrowserUserAgent import GetHeader
from fake_useragent import UserAgent
from urllib.parse import urlencode
import os
import errno

from io import StringIO
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

def GetDataFrameByCssSelector(url, css_selector, index = None):
    #print(css_selector)
    # Configure Chrome options
    chrome_options = Options()
    # Configure Chrome options
    #chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    #chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    #chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
#
    # Initialize the WebDriver with the specified options
    # The ChromeDriverManager automatically downloads the driver version required by the current version of Chrome installed on your system
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    driver.refresh()
    # Wait for the necessary time for the page to load
    #driver.implicitly_wait(15)  # Adjust the time according to your needs
    WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))


    # Now you can use BeautifulSoup or Selenium to parse the page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    data = soup.select_one(css_selector)
    #print(data)
    try:
        dfs = pd.read_html(StringIO(data.prettify()))
    except:
        return pd.DataFrame()

    #print(dfs)
    
    if index is not None and index < len(dfs):
        return dfs[index]

    for df in dfs:
        if len(df) > 1:
            return df
    return None 

def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def GetDataByXPath(htmlInfo, XPath):
    return htmlInfo.xpath(re.sub(r"/tbody([[]\\d[]])?", "", XPath) + "/text()")[0]


def WriteFile(filePath, content):
    # 建立資料夾, 如果資料夾不存在時
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filePath, "w", encoding="utf-8-sig") as file:
        file.write(content)


def GetYearBetween(startDateStr, endDate=datetime.today()):
    date_format = "%Y%m%d"
    startDate = datetime.strptime(str(startDateStr), date_format)
    delta = endDate - startDate
    years = round(delta.days / 365)
    # print(years)
    return years


# 取得dataframe比對相等(含有字元), 第一欄值


def GetDataFrameValueByLabel(df, columnLable, matchRowLable):
    return df.set_index(columnLable).filter(like=matchRowLable, axis=0).values[0]

'''
def GetDataFrameByCssSelector(url, css_selector):
    rawData = requests.get(url, headers=GetHeader())
    rawData.encoding = "utf-8"
    return BeautifulSoup2DataFrame(rawData, css_selector)
'''

def PostDataFrameByCssSelector(url_root, payload, css_selector):
    qs = urlencode(payload)
    url = f"{url_root}?{qs}"

    ua = UserAgent()
    headers = {"user-agent": ua.random, "referer": url}

    rawData = requests.post(url, headers=headers)
    # rawData.encoding = 'utf-8'
    return BeautifulSoup2DataFrame(rawData, css_selector)


# BeautifulSoup資料轉成DataFrame
def BeautifulSoup2DataFrame(rawData, css_selector):
    soup = BeautifulSoup(rawData.text, "html.parser")
    data = soup.select_one(css_selector)
    try:
        dfs = pd.read_html(data.prettify())
    except:
        return pd.DataFrame()

    # print(dfs)
    if len(dfs[0]) > 1:
        return dfs[0]
    if len(dfs[1]) > 1:
        return dfs[1]
    return dfs


def delete_folder(path):
    for sub in path.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    path.rmdir()

'''
https://www.finlab.tw/python-%E8%B2%A1%E5%A0%B1%E7%88%AC%E8%9F%B2-1-%E7%B6%9C%E5%90%88%E6%90%8D%E7%9B%8A%E8%A1%A8/
'''
def GetFinancialStatement(type='綜合損益'):
    # 判斷是哪個年度第幾季
    # 參考: https://www.nstock.tw/author/article?id=184
    now = date.today()
    current_year = now.year
    roc_year = current_year - 1911
    season = 0

    last_q4_day = date(current_year, 3, 31)  # 前一年度第四季
    q1_day = date(current_year, 5, 15)  # 第一季(Q1)財報：5/15前
    q2_day = date(current_year, 8, 14)  # 第二季(Q2)財報：8/14前
    q3_day = date(current_year, 11, 14)  # 第三季(Q3)財報：11/14前
    q4_day = date(current_year + 1, 3, 31)  # 第四季(Q4)財報及年報：隔年3/31前

    if now <= last_q4_day:
        roc_year -= 1
        season = 3
    elif now <= q1_day and now > last_q4_day:
        roc_year -= 1
        season = 4
    elif now <= q2_day and now > q1_day:
        season = 1
    elif now <= q3_day and now > q2_day:
        season = 2
    elif now <= q4_day and now > q3_day:
        season = 3

        
    if type == '綜合損益':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')

    form_data = {
        "encodeURIComponent": 1,
        "step": 1,
        "firstin": 1,
        "off": 1,
        "TYPEK": "sii",
        "year": roc_year,
        "season": season,
    }

    response = requests.post(url, form_data)
    response.encoding = "utf8"

    soup = BeautifulSoup(response.text, "html.parser")
    # print(response.text)
    # df = translate_dataFrame(response.text)
    if not soup.find(text=re.compile("查詢無資料")):
        df_table = pd.read_html(response.text)
        df = df_table[0]
        # df.columns = df.columns.get_level_values(0)
        # print(df.columns)
        df = df.drop_duplicates(keep=False, inplace=False)

        return pd.concat(df[1:], axis=0, sort=False)\
             .set_index(['公司代號'])\
             .apply(lambda s: pd.to_numeric(s, errors='ceorce'))

    return pd.DataFrame()