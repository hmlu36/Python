import requests
import re
from lxml import etree

url = "https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID=5515&CHT_CAT=WEEK"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}


resInfo = requests.get(url, headers=headers)
resInfo.encoding = 'utf-8'
htmlInfo = etree.HTML(resInfo.text)

header = ['EPS', 'PE_now']
for index in range(1, 5, 1):
    XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[142]/td[{index}]/nobr'
    entry = htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]
    header.append(entry)
print(header)

data = []
for index in range(5, 12, 1):
    #print(index)
    XPath = f'/html/body/table[2]/tbody/tr/td[3]/div/div/div/table/tbody/tr[3]/td[{index}]'
    #print(XPath)

    entry = htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]
    data.append(entry)

print(data)
for index in range(len(header)):
    print(header[index] + ': ' + data[index])
