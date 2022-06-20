# basic
import numpy as np
import pandas as pd

# get data
import pandas_datareader as pdr

# visual
import matplotlib.pyplot as plt
import seaborn as sns

#requests
import requests

'''
參考: 
    https://ithelp.ithome.com.tw/articles/10204773
    https://www.knowslist.com/a/uebLajubb6o
'''


def remove_td(column):
    remove_one = column.split('<')
    remove_two = remove_one[0].split('>')
    return remove_two[1].replace(",", "")

def translate_dataFrame(response):
     # 拆解內容
    table_array = response.split('<table')
    tr_array = table_array[1].split('<tr')
    
    # 拆解td
    data = []
    index = []
    column = []
    for i in range(len(tr_array)):
        td_array = tr_array[i].split('<td')
        if(len(td_array)>1):
            code = remove_td(td_array[1])
            name = remove_td(td_array[2])
            revenue  = remove_td(td_array[3])
            profitRatio = remove_td(td_array[4])
            profitMargin = remove_td(td_array[5])
            preTaxIncomeMargin = remove_td(td_array[6])
            afterTaxIncomeMargin = remove_td(td_array[7])
            if(type(code) == float):
                data.append([code, revenue, profitRatio, profitMargin, preTaxIncomeMargin, afterTaxIncomeMargin])
                index.append(name)
            if( i == 1 ):
                column.append(code)
                column.append(revenue)
                column.append(profitRatio)
                column.append(profitMargin)
                column.append(preTaxIncomeMargin)
                column.append(afterTaxIncomeMargin)
                
    return pd.DataFrame(data=data, index=index, columns=column)

def financial_statement(year, season):
    if year >= 1000:
        year -= 1911
        
    url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
    form_data = {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year': year,
        'season': season,
    }

    response = requests.post(url,form_data)
    response.encoding = 'utf8'
    
    df = translate_dataFrame(response.text)
    return df

stock = financial_statement(2022,1)
stock = stock.astype(float)
print(stock)