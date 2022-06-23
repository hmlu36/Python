# basic
from asyncio.windows_events import NULL
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import date

# get data
import pandas_datareader as pdr

# visual
import matplotlib.pyplot as plt
import seaborn as sns

# requests
import requests

'''
參考: 
    https://ithelp.ithome.com.tw/articles/10204773
    https://www.knowslist.com/a/uebLajubb6o
'''


def financial_statement(year, season, type):
    if year >= 1000:
        year -= 1911

        
    if type == '綜合損益':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')


    url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
    form_data = {
        'encodeURIComponent': 1,
        'step': 1,
        'firstin': 1,
        'off': 1,
        'TYPEK': 'sii',
        'year': year,
        'season': season,
    }

    response = requests.post(url, form_data)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, "html.parser")
    #print(response.text)
    #df = translate_dataFrame(response.text)
    if not soup.find(text=re.compile('查詢無資料')):
        df_table = pd.read_html(response.text)
        print(df_table)
        df = df_table[0]
        df.columns = df.columns.get_level_values(0)
        print(df.columns)
        df = df.drop_duplicates(keep=False, inplace=False)
        '''
        df.columns = ['公司代號', '公司名稱', '營業收入', '毛利率', '營業利益率', '稅前純益率', '稅後純益率']
        df['營業收入'] = df['營業收入'].astype(float) / 100
        df.update(df.apply(lambda x : pd.to_numeric(x,errors='coerce')))
        '''
        return df

    return pd.DataFrame()



temp_date = date(2022, 3, 1)
now = date.today()
current_year = now.year 
roc_year = current_year - 1911
season = 0

last_q4_day = date(current_year, 3, 31)
print(last_q4_day)

q1_day = date(current_year, 5, 15) # 第一季(Q1)財報：5/15前
print(q1_day)

q2_day = date(current_year, 8, 14) # 第二季(Q2)財報：8/14前
print(q2_day)

q3_day = date(current_year, 11, 14) # 第三季(Q3)財報：11/14前
print(q3_day)

q4_day = date(current_year + 1, 3, 31) # 第四季(Q4)財報及年報：隔年3/31前
print(q4_day)

if temp_date <= last_q4_day:
    roc_year -= 1
    season = 3
elif  temp_date <= q1_day and temp_date > last_q4_day:
    roc_year -= 1
    season = 4
elif  temp_date <= q2_day and temp_date > q1_day:
    season = 1
elif  temp_date <= q3_day and temp_date > q2_day:
    season = 2
elif  temp_date <= q4_day and temp_date > q3_day:
    season = 3

print(roc_year)
print(season)

stock = financial_statement(111, 1, '資產負債')
print(stock)
'''
cond1 = stock['毛利率'] > 30
cond2 = stock['營業利益率'] > 30
print(stock[cond1 & cond2])
plt.rcParams['axes.unicode_minus']=False
fig = plt.figure(figsize=(10, 6))
stock['毛利率'].hist(bins=range(-100,100) , label="毛利率")
plt.legend()
plt.show()
'''
#print(stock.loc[(stock['公司名稱'] == '台積電')])
