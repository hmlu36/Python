from fake_useragent import UserAgent
from BrowserUserAgent import GetHeader
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time
import requests

def GetDistributionSummaryTable():
    url='https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'
    #url = 'TDCC_OD_1-5.csv'
    df = pd.read_csv(url)

    # 列轉成欄位
    # 參考 https://stackoverflow.com/questions/63413708/transforming-pandas-dataframe-convert-some-row-values-to-columns
    df['key2']=(df.groupby('證券代號').cumcount()+1)
    s = df.set_index(['資料日期','證券代號','key2']).unstack().sort_index(level=1,axis=1)
    s.columns=s.columns.map('{0[0]}_{0[1]}'.format)
    s = s.rename_axis([None], axis=1).reset_index()
    #s.to_csv('股東分布資料.csv',encoding='utf_8_sig')
    #print(s)

    retailHeaders = ['1-999','1,000-5,000','5,001-10,000','10,001-15,000','15,001-20,000','20,001-30,000','30,001-40,000','40,001-50,000','50,001-100,000']
    distributionRangeHeaders = retailHeaders + ['100,001-200,000','200,001-400,000','400,001-600,000','600,001-800,000','800,001-1,000,000','1,000,001', '差異數調整', '合計']
   
    newTitle = ['資料日期','證券代號'] + [distribution + title for distribution in distributionRangeHeaders for title in ['人數','比例','持股分級','股數']]
    #print(newTitle)
    s.columns = newTitle

    #print(s)
    s['100張以下比例'] = s[[retailHeader + title for retailHeader in retailHeaders for title in ['比例']]].sum(axis=1)
    s['100張以下人數'] = s[[retailHeader + title for retailHeader in retailHeaders for title in ['人數']]].sum(axis=1)
    s = s.rename(columns = {'100,001-200,000比例': '101-200張比例', '100,001-200,000人數': '101-200張人數', 
                            '200,001-400,000比例': '201-400張比例', '200,001-400,000人數': '201-400張人數', 
                            '400,001-600,000比例': '401-600張比例', '400,001-600,000人數': '401-600張人數', 
                            '600,001-800,000比例': '601-800張比例', '600,001-800,000人數': '601-800張人數', 
                            '800,001-1,000,000比例': '801-1000張比例', '800,001-1,000,000人數': '801-1000張人數', 
                            '1,000,001比例':'1000張以上比例', '1,000,001人數':'1000張以上人數'})
    s['401-800張人數'] = s[['401-600張人數', '601-800張人數']].sum(axis=1)
    s['401-800張比例'] = s[['401-600張比例', '601-800張比例']].sum(axis=1)
    #print(s.columns)
    s = s[['證券代號', '100張以下人數', '100張以下比例', 
           '101-200張人數', '101-200張比例', 
           '201-400張人數', '201-400張比例', 
           '401-800張人數', '401-800張比例', 
           '801-1000張人數', '801-1000張比例', 
           '1000張以上人數', '1000張以上比例']]

    print(s)
    #s.to_csv('股東分布資料.csv',encoding='utf_8_sig')
    return s

    
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


#總表
#GetDistributionSummaryTable()
# 個股(含歷程)
df = GetDistribution('8112')
print(df)