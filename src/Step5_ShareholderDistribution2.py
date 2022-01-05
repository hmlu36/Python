
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import re
from BrowserUserAgent import GetHeader
from fake_useragent import UserAgent
import random
import Utils
import time


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


def GetDirectorSharehold(stockId):
    cssSelector = '#divStockList'
    sum_df = pd.DataFrame()

    for rankIndex in range(1, 6):
        url = f'https://goodinfo.tw/tw/StockList.asp?SHEET=董監持股&MARKET_CAT=熱門排行&INDUSTRY_CAT=全體董監持股比例&RANK={str(rankIndex)}'
        print(url)

        try:
            #time.sleep(random.randint(20, 30))
            df = Utils.GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            sum_df = pd.concat([sum_df, df], axis=0)
            #df.columns = df.columns.get_level_values(1)
        except:
            #time.sleep(random.randint(20, 30))
            df = Utils.GetDataFrameByCssSelector(url, cssSelector)
            print(df)
            #df.columns = df.columns.get_level_values(1)

    sum_df.to_csv('董監持股比例.csv',encoding='utf_8_sig')

GetDirectorSharehold('2330')

'''
df = GetDistribution('8112')
print(df)
'''
