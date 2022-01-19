import Utils
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from BrowserUserAgent import GetHeader
import UtilsCaptcha
import json
import time
from datetime import date
import random
from functools import reduce
import operator
import os
import errno

# 參考 
# https://gist.github.com/CMingTseng/79447ccb2bb41e4bd8ec36d020fccab9
# https://github.com/Pregaine/stock/blob/master/01_Day%20process/%E5%88%B8%E5%95%86%E5%88%86%E9%BB%9E/%E6%8D%89%E5%8F%96%E5%8D%B7%E5%95%86%E8%B2%B7%E8%B3%A3.py
# 公式 範例
# https://blog.cnyes.com/my/uniroselee/article2270853

base_url = 'https://bsr.twse.com.tw/bshtm'
path = f'{Utils.GetRootPath()}\Data\Daily\Chip'

#交易日期
receive_date = ''

#成交筆數
trade_rec = 0

#成交金額
trade_amt = 0

def DownloadVolume(stockId):
    session = requests.Session()
    headers = GetHeader()
    response = session.get(f'{base_url}/bsMenu.aspx', headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 辨識Captcha
        img_url = soup.findAll('img')[1]['src']
        print(img_url)

        img = UtilsCaptcha.GetCaptcha(f'{base_url}/{img_url}')
        captcha = UtilsCaptcha.DecodeCaptcha(img)
        print('captcha: ' + captcha)

        params = {}

        # 取得頁面上session參數資料
        nodes = soup.select('form input')
        for node in nodes:
            name = node.attrs['name']

            # 忽略鉅額交易的 radio button
            if name in ('RadioButton_Excd', 'Button_Reset'):
                continue

            if 'value' in node.attrs:
                params[node.attrs['name']] = node.attrs['value']
            else:
                params[node.attrs['name']] = ''

        params['CaptchaControl1'] = captcha
        params['TextBox_Stkno'] = stockId

        # 送出
        #print(json.dumps(params, indent=2))
        resp = session.post(f'{base_url}/bsMenu.aspx', data=params, headers=headers)
        if resp.status_code != 200:
            print('任務失敗: %d' % resp.status_code)
            return { 'success' : False }
            
        soup = BeautifulSoup(resp.text, 'lxml')
        errorMessage = soup.select('#Label_ErrorMsg')[0].get_text()

        if errorMessage: 
            print('錯誤訊息: ' + errorMessage)
            return { 'success' : False }
        else :
            nodes = soup.select('#HyperLink_DownloadCSV')
            if len(nodes) == 0:
                print('任務失敗，沒有下載連結')
                return { 'success' : False }
            
            # 下載分點進出 CSV
            resp = session.get(f'{base_url}/bsContent.aspx')
            if resp.status_code != 200:
                print('任務失敗，無法下載分點進出 CSV')
                return { 'success' : False }

            #print(resp.text)
            resp = session.get(f'{base_url}/bsContent.aspx?v=t')
            soup = BeautifulSoup(resp.text, 'html.parser')

            #交易日期
            receive_date = soup.select_one('#receive_date').text.replace('/', '').strip()

            #成交筆數
            trade_rec = soup.select_one('#trade_rec').text.strip()

            #成交金額
            trade_amt = soup.select_one('#trade_amt').text.strip()
            
            print('receive_date:' + receive_date + ', trade_rec:' + trade_rec + ', trade_amt:' + trade_amt)

            #重組table(取出class有column_value_price_2, column_value_price_3)
            trs = soup.find_all("tr", {"class": ["column_value_price_2", "column_value_price_3"]})
            #print(str(trs))

            soup = BeautifulSoup(f'<table>{str(trs)}</table', 'html.parser')
            data = soup.select_one('table')
            df = pd.read_html(data.prettify())[0]
            df.columns=['序號', '券商', '價格', '買進股數', '賣出股數']
            df.dropna(subset=['券商'],inplace=True) # 移除空白列
            df['買進股數'] = df['買進股數'].astype(int)
            df['賣出股數'] = df['賣出股數'].astype(int)
            
            # 去掉中文和空白
            df["券商"] = df['券商'].replace(regex=r'[\u4e00-\u9fa5]',value='').replace(regex=r' +$',value='') 
            #print(df)
            
            # 寫檔案
            filePath = f'{path}\{receive_date}\{stockId}.csv'
            # 建立資料夾, 如果資料夾不存在時 
            if not os.path.exists(os.path.dirname(filePath)):
                try:
                    os.makedirs(os.path.dirname(filePath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            df.to_csv(filePath,encoding='utf_8_sig') 
            
            return { 
                'success' : True,
                'receive_date': receive_date,
                'trade_rec': trade_rec,
                'trade_amt': trade_amt
            }
            
def GetVolumeIndicator(result, stockId):
    df = pd.read_csv(f'{path}\{result["receive_date"]}\{stockId}.csv')
    
    # TOP 1 買超 = 買最多股票的券商 買多少
    top1Buy = df['買進股數'].max()

    # TOP 1 賣超 = 賣最多股票的券商 賣多少
    top1Sell = df['賣出股數'].max()
    # 超額買超 = TOP 1 買超 / TOP 1 賣超
    overBuy = round(top1Buy / top1Sell, 2)

    # 重押比例 > 30%
    top1BuyPercent = (top1Buy / 1000) / float(result['trade_rec'].replace(',', ''))
    print("top1BuyPercent:" + str(top1BuyPercent))
    allInSecurities = ''
    if (top1BuyPercent) > 0.3:
        mainSecurities = df[df['買進股數'] == df['買進股數'].max()]['券商'].values[0]
        print('主要券商:' + mainSecurities)
        allInSecurities = mainSecurities + ' (' + str(round(top1BuyPercent * 100, 3)) + '%) ' 
                
    # 買超張數 > 500, 買超異常4倍                
    if overBuy > 4.0 and (top1Buy / 1000 > 500):
        overBuy = '🏆' + str(overBuy)
    elif overBuy < 0.25 and (top1Sell / 1000 > 500):
        overBuy = '⚠️' + str(overBuy)
        
    print('top1Buy:' + str(top1Buy) + ', top1Sell:' + str(top1Sell) + ', overBuy:' + str(overBuy));
    
    # 買方的前 15 名買超量 
    top15Buy = df.sort_values('買進股數', ascending=False).head(15)['買進股數'].sum()
    # 賣方的前 15 名賣超量
    top15Sell = df.sort_values('賣出股數', ascending=False).head(15)['賣出股數'].sum()
    # 前15名買賣超量 = 買方的前 15 名買超量 - 賣方的前 15 名賣超量
    top15Volume = top15Buy - top15Sell
    #print('top15Buy:' + str(top15Buy) + ', top15Sell:' + str(top15Sell) + ', volumeFloat:' + str(volumeFloat))
    
    # 總成交量
    totalVolume = df['買進股數'].sum()

    # 前15名買賣超量集中度(%) = 前15名買賣超量 ÷ 總成交量
    top15VolumeRate = round(top15Volume / totalVolume * 100, 2)
    prefixIcon = ''

    # 前15卷商籌碼集中度 > 20%
    if top15VolumeRate > 20:
        prefixIcon = '🏆'
    elif top15VolumeRate < -10:
        prefixIcon = '⚠️' 
    top15VolumeRate = prefixIcon + str(top15VolumeRate)
    print('totalVolume:' + str(totalVolume) + ', top15Volume:' + str(top15Volume) + ', top15VolumeRate:' + str(top15VolumeRate))


    # 買賣家數差 = 買進券商數 - 賣出券商數
    buySecuritiesCount = np.count_nonzero(df['買進股數'])
    sellSecuritiesCount = np.count_nonzero(df['賣出股數'])
    print('buySecuritiesCount:' + str(buySecuritiesCount) + ', sellSecuritiesCount:' + str(sellSecuritiesCount))
    return pd.DataFrame([[overBuy, allInSecurities, top15VolumeRate]], columns=['超額買超', '重押券商', '前15卷商籌碼集中度'])

def GetVolume(stockId):
    error_count = 0
    max_error_count = 10 #最多10次
    while error_count < max_error_count:
        try:
            result = DownloadVolume(stockId)
            if result['success']:
                return GetVolumeIndicator(result, stockId)
            else:
                time.sleep(random.randint(1, 5))
                error_count = error_count + 1
                print(f'錯誤次數{error_count}')
                
        except Exception as e:
            print(str(e))

'''
#df = GetVolumeIndicator('8112')
df = GetVolume('1604')
print(df)
'''