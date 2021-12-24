import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from lxml import etree


url = "https://concords.moneydj.com/Z/ZC/ZCX/ZCX_2069.djhtm"
#url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT2=DATE"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}
#res = requests.get(url,headers = headers)
data = pd.read_html(url)
print(data)
#res.encoding = "utf-8"
#soup = BeautifulSoup(res.text,"lxml")
#data = soup.findAll("table")
#data = soup.select_one("#divK_ChartDetail")
#print(data)
#df = pd.read_html(data.prettify())
#print(df)

#res.encoding = 'utf-8'