import re
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
from BrowserUserAgent import GetHeader
from fake_useragent import UserAgent
from urllib.parse import urlencode
import os
import errno
import pathlib

def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

def GetDataByXPath(htmlInfo, XPath):
    return htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]

def WriteFile(filePath, content):
    # 建立資料夾, 如果資料夾不存在時 
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filePath, 'w', encoding='utf-8-sig') as file:
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

def GetDataFrameByCssSelector(url, css_selector):
    rawData = requests.get(url, headers=GetHeader())
    rawData.encoding = 'utf-8'
    return BeautifulSoup2DataFrame(rawData, css_selector)

def PostDataFrameByCssSelector(url_root, payload, css_selector):
    qs = urlencode(payload)
    url = f'{url_root}?{qs}'

    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
        'referer': url
    }

    rawData = requests.post(url, headers=headers)
    #rawData.encoding = 'utf-8'
    return BeautifulSoup2DataFrame(rawData, css_selector)

# BeautifulSoup資料轉成DataFrame
def BeautifulSoup2DataFrame(rawData, css_selector):
    soup = BeautifulSoup(rawData.text, "html.parser")
    data = soup.select_one(css_selector)
    try:
        dfs = pd.read_html(data.prettify())
    except:
        return pd.DataFrame()
        
    #print(dfs)
    if len(dfs[0]) > 1:
        return dfs[0]
    if len(dfs[1]) > 1:
        return dfs[1]
    return dfs

def delete_folder(path) :
    for sub in path.iterdir() :
        if sub.is_dir() :
            delete_folder(sub)
        else :
            sub.unlink()
    path.rmdir() # if you just want to delete the dir content but not the dir itself, remove this line