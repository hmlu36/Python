import requests
from fake_useragent import UserAgent
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import Utils

url_root = 'https://goodinfo.tw/StockInfo/ShowK_Chart.asp'

payload = {
    'STOCK_ID': '0050',
    'CHT_CAT2': 'DATE',
    'STEP': 'DATA',
    'PERIOD': 365
}
attrs = {'id': 'tblPriceDetail'}

df = Utils.PostDataFrameByAttrs(url_root, payload, attrs)
print(df)

'''
k_data = []
print(rows)
for row in rows:
    columns = row.select('td')
    print(columns)
    k_data.append({
        'day': columns[0].get_text(strip=True),
        'open_price': float(columns[1].get_text(strip=True)),
        'high_price': float(columns[2].get_text(strip=True)),
        'low_price': float(columns[3].get_text(strip=True)),
        'close_price': float(columns[4].get_text(strip=True))
    })
    
print(k_data)
'''