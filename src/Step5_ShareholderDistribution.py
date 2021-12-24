from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time


def GetDistribution():
    #url='https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'
    url = 'TDCC_OD_1-5.csv'
    df = pd.read_csv(url)

    # 列轉成欄位
    # 參考 https://stackoverflow.com/questions/63413708/transforming-pandas-dataframe-convert-some-row-values-to-columns
    df['key2']=(df.groupby('證券代號').cumcount()+1)
    s = df.set_index(['資料日期','證券代號','key2']).unstack().sort_index(level=1,axis=1)
    s.columns=s.columns.map('{0[0]}_{0[1]}'.format)
    s = s.iloc[2:]
    #s.to_csv('股東分布資料.csv',encoding='utf_8_sig')
    print(s)
    
    distributionRange = ['1-999','1,000-5,000','5,001-10,000','10,001-15,000','15,001-20,000','20,001-30,000','30,001-40,000','40,001-50,000','50,001-100,000','100,001-200,000','200,001-400,000','400,001-600,000','600,001-800,000','800,001-1,000,000','1,000,001', '差異數調整', '合計']
   
    newTitle = ['資料日期','證券代號'] + [distribution + title for distribution in distributionRange for title in ['人數','比例','持股分級','股數']]
    print(newTitle)
    s.columns = newTitle

    extractTitle = [distribution + title for distribution in distributionRange for title in ['比例']]
    #print(extractTitle)
    extractTitle.insert(0, '證券代號')
    print(extractTitle)
    print(s)
    s = s[s[extractTitle]]
    s.to_csv('股東分布資料.csv',encoding='utf_8_sig')

GetDistribution()




'''
def GetDistribution(stockId):
    url = f'https://goodinfo.tw/tw/EquityDistributionClassHis.asp?STOCK_ID={stockId}'
    cssSelector = '#divDetail'
    try:
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(1)
    except:
        time.sleep(random.randint(20, 30))
        df = Utils.GetDataFrameByCssSelector(url, cssSelector)
        df.columns = df.columns.get_level_values(1)
    
    # 千張大戶
    data = pd.to_numeric(df['＞1千張'], errors='coerce').dropna(how='any',axis=0).head(3)
    return ' / '.join(map(str, list(data)))
'''
'''
data = GetDistribution('1515')
print(data)
'''