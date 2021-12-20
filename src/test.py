import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=CF_M_QUAR_ACC&STOCK_ID=2330"
#url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT2=DATE"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}
res = requests.get(url,headers = headers)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text,"lxml")
data = soup.select_one("#divFinDetail")
#data = soup.select_one("#divK_ChartDetail")
df = pd.read_html(data.prettify())
print(len(df[0]))
print(len(df[1]))
#print(df[1])

#print(df)