
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
from BrowserUserAgent import GetHeader

def GetDistribution(stockId):
    url = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
    today = datetime.today()
    dateFormat = '%Y/%m/%d'
    startDateStr = (today - timedelta(days=30)).strftime(dateFormat)
    endDateStr = today.strftime(dateFormat)
    print('startDate:' + startDateStr + ', endDate:' + endDateStr)
    # 產生日期區間
    datePeriod = pd.date_range(startDateStr, endDateStr, freq='W-FRI')[::-1]
    tempDate = datePeriod[0].strftime('%Y%m%d')

    payload = {
        'scaDates': tempDate,
        'scaDate': tempDate,
        'SqlMethod': 'StockNo',
        'StockNo': stockId,
        'StockName': '',
        'REQ_OPR': 'SELECT',
        'clkStockNo': stockId,
        'clkStockName': ''
    }

    rawData = requests.post(url, data=payload, headers=GetHeader())

    soup = BeautifulSoup(rawData.text, 'html.parser')
    tb = soup.select('.mt')[1]
    all_data = []
    for tr in tb.select('tr'):
        rdata = [td.text.replace("\u3000","").replace(",","").strip() for td in tr.select('td')]
        all_data.append(rdata)

    ls_head = ['SEQ', 'LV_DESC', 'NUM_OF_PEOPLE', 'STOCK_SHARES', 'PER_CENT_RT']
    df = pd.DataFrame(all_data[1:len(all_data)-1], columns=ls_head)	#最後一筆合計資料不要
    df.to_csv('股東分布資料.csv',encoding='utf_8_sig')
    #df = pd.DataFrame(all_data[1:], columns=ls_head)	#最後一筆合計資料不要
    #print(df)
    header = df['LV_DESC'].tolist()
    df = df[['NUM_OF_PEOPLE', 'PER_CENT_RT']].T
    print(df.iloc[0:1, 0:9])
    people100 = df.iloc[0:1, 0:9].astype(int).sum(axis=1)
    #print(people100)
    people100_10000 = df.iloc[0:1, 9:14].astype(int).sum(axis=1)
    #print(people100_10000)

    print(df.iloc[0:1, 14:15])
    people10000 = df.iloc[0:1, 14:15].astype(int).sum(axis=1)
    print(people10000)
    #df['100-1000張人數'] = df[['1-999', '1000-5000', '5001-10000', '10001-15000', '15001-20000', '20001-30000', '30001-40000', '40001-50000', '50001-100000']].sum(axis=1)

    data = []
    for index, option in enumerate(['int','float']):
        lastCnt = 0
        for cnt in [9, 14, 15]:
            #print('index:' + str(index) + ', cnt:' + str(cnt))
            sum = df.iloc[index: index+1, lastCnt : cnt].astype(option).sum(axis=1)
            data.append(sum)
            lastCnt = cnt

    print(data)
    return df

df = GetDistribution('8112')
print(df)