
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
from BrowserUserAgent import GetHeader
from fake_useragent import UserAgent

def GetDistribution(stockId):
    url = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'
    # print(rawData.text)
    # 取得日期下拉選單
    payload = {
        'REQ_OPR': 'qrySelScaDates',
    }

    dates = requests.post(url, data=payload, headers=GetHeader()).json()
    # print(dates)

    '''
    產生日期區間
    today = datetime.today()
    dateFormat = '%Y/%m/%d'
    startDateStr = (today - timedelta(days=30)).strftime(dateFormat)
    endDateStr = today.strftime(dateFormat)
    # 產生日期區間
    datePeriod = pd.date_range(startDateStr, endDateStr, freq='W-FRI')[::-1]
    print('startDate:' + startDateStr + ', endDate:' + endDateStr + ', loopDate:' + datePeriod[0])
    tempDate = datePeriod[2].strftime('%Y%m%d')
    '''

    sum_df = pd.DataFrame()

    for date in dates[:5]:
        #print('date:' + date)
        payload = {
            'scaDates': date,
            'scaDate': date,
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
            rdata = [td.text.replace("\u3000", "").replace(
                ",", "").strip() for td in tr.select('td')]
            all_data.append(rdata)

        ls_head = ['SEQ', 'LV_DESC', 'NUM_OF_PEOPLE',
                   'STOCK_SHARES', 'PER_CENT_RT']
        df = pd.DataFrame(all_data[1:len(all_data)-1],
                          columns=ls_head)  # 最後一筆合計資料不要
        # df.to_csv('股東分布資料.csv',encoding='utf_8_sig')
        # df = pd.DataFrame(all_data[1:], columns=ls_head)	#最後一筆合計資料不要
        # print(df)

        #header = df['LV_DESC'].tolist()
        # print(header)

        df = df[['NUM_OF_PEOPLE', 'PER_CENT_RT']]
        # print(df)
        '''
        print(df.iloc[0:1, 0:9])
        people100 = df.iloc[0:1, 0:9].astype(int).sum(axis=1)
        print(people100)
        people100_10000 = df.iloc[0:1, 9:14].astype(int).sum(axis=1)
        print(people100_10000)

        print(df.iloc[0:1, 14:15])
        people10000 = df.iloc[0:1, 14:15].astype(int).sum(axis=1)
        print(people10000)
        '''
        #df['100-1000張人數'] = df[['1-999', '1000-5000', '5001-10000', '10001-15000', '15001-20000', '20001-30000', '30001-40000', '40001-50000', '50001-100000']].sum(axis=1)

        rangeDicts = {'100張以下': 9, '100-1000張': 14, '1000張以上': 15}
        # print(df['NUM_OF_PEOPLE'].iloc[0:9])

        row = {}
        for typeKey, typeValue in {'NUM_OF_PEOPLE': 'int', 'PER_CENT_RT': 'float'}.items():
            previousCnt = 0

            for rangeIndex, (rangeKey, rangeValue) in enumerate(rangeDicts.items()):
                #print('previousCnt:' + str(previousCnt) + ', rangeValue:' + str(rangeValue))
                sum = df[typeKey].iloc[previousCnt: rangeValue].astype(
                    typeValue).sum(axis=0)
                # 有小數時, 四捨五入小數第二位
                sum = round(sum, 0 if typeValue == 'int' else 2)

                # print(sum)
                header = rangeKey + ('人數' if typeKey ==
                                     'NUM_OF_PEOPLE' else '比例')
                row.update({header: sum})
                if rangeIndex == len(rangeDicts) - 1:
                    previousCnt = rangeValue + 1
                else:
                    previousCnt = rangeValue

        # print(row)
        sum_df = sum_df.append(row, ignore_index=True)

    #將dataframe資料轉成 / 串起來
    data = {}
    for column in sum_df.columns.values:
        #print(column + ', data:' + '/'.join(sum_df[column].astype(str)))
        data.update({column: '  /  '.join(sum_df[column].astype(str))})

    df = pd.DataFrame([data])
    # print(df)
    return df


def GetDirectorSharehold2(stockId):
    url = 'https://goodinfo.tw/tw/StockList.asp?SHEET=董監持股&MARKET_CAT=熱門排行&INDUSTRY_CAT=全體董監持股比例'
    rawData = requests.get(url, headers=GetHeader())
    rawData.encoding = 'utf-8'
    print(rawData.text)

def GetDirectorSharehold(stockId):
    url = 'https://goodinfo.tw/tw/StockList.asp?SHEET=%E8%91%A3%E7%9B%A3%E6%8C%81%E8%82%A1&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%85%A8%E9%AB%94%E8%91%A3%E7%9B%A3%E6%8C%81%E8%82%A1%E6%AF%94%E4%BE%8B&RANK=5'
    url = f'https://goodinfo.tw/tw/StockList.asp'
    payload = {
        'SEARCH_WORD': '',
        'SHEET': '董監持股',
        'SHEET2': '',
        'MARKET_CAT': '熱門排行',
        'INDUSTRY_CAT': '全體董監持股比例(%)@@全體董監@@持股比例(%)',
        'STOCK_CODE': '',
        'RPT_TIME': '最新資料',
        'STEP': 'DATA',
        'RANK':	5
    }

    response = requests.get(url, headers=GetHeader())
    cookies = response.cookies
    print(cookies.items)

    rawData = requests.post(url, data=payload, cookies=cookies, headers={'user-agent': UserAgent().random, 'Referer': 'https://goodinfo.tw/'})
    print(rawData.text)


GetDirectorSharehold2('2330')

'''
df = GetDistribution('8112')
print(df)
'''
