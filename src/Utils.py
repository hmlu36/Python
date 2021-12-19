import re
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
from BrowserUserAgent import GetHeader
from fake_useragent import UserAgent
from urllib.parse import urlencode


def GetDataByXPath(htmlInfo, XPath):
    return htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]


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


def GetDataFrameByAttrs(url, attrs):
    rawData = requests.get(url, headers=GetHeader())
    rawData.encoding = 'utf-8'
    soup = BeautifulSoup(rawData.text, "html.parser")
    return BeautifulSoup2DataFrame(url, soup, attrs)

def PostDataFrameByAttrs(url_root, payload, attrs):
    qs = urlencode(payload)
    url = f'{url_root}?{qs}'

    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
        'referer': url
    }

    response = requests.post(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    return BeautifulSoup2DataFrame(url, soup, attrs)

#BeautifulSoup資料轉成DataFrame
def BeautifulSoup2DataFrame(url, soup, attrs):
    # 參考
    # https://stackoverflow.com/questions/50633050/scrape-tables-into-dataframe-with-beautifulsoup
    table = soup.find('table', attrs=attrs)
    table_rows = table.find_all('tr')
    
    headers = []
    rows = []
    for index, tr in enumerate(table_rows):
        print(tr)
        td = tr.find_all('th') + tr.find_all('td')
        row = [tr.text.strip().replace('\n', '').replace('\xa0', '')
               for tr in td if tr.text.strip()]
        if row:
            if index == 0:
                headers.append(row)
            else:
                rows.append(row)

    # 本益比河流圖有跨欄, 需額外處理(將跨欄標題合併同一行)
    if any(x in url for x in ['ShowK_ChartFlow', 'ShowK_Chart']):
        del headers[0][-1] # 刪除跨欄標題
        headers[0].extend(rows[0]) #加入第二行跨欄標題
        del rows[0] # 刪除第二行

    #print(headers)
    #print(rows)
    df = pd.DataFrame(rows, columns=headers)
    return df
