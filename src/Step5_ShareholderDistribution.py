from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import Utils
import pandas as pd
import random
import time


def GetDistribution():
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
    s.to_csv('股東分布資料.csv',encoding='utf_8_sig')

GetDistribution()
