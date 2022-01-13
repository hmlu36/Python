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

# 參考 
# https://gist.github.com/CMingTseng/79447ccb2bb41e4bd8ec36d020fccab9
# https://github.com/Pregaine/stock/blob/master/01_Day%20process/%E5%88%B8%E5%95%86%E5%88%86%E9%BB%9E/%E6%8D%89%E5%8F%96%E5%8D%B7%E5%95%86%E8%B2%B7%E8%B3%A3.py
# 公式 範例
# https://blog.cnyes.com/my/uniroselee/article2270853

base_url = 'https://bsr.twse.com.tw/bshtm'
path = f'{Utils.GetRootPath()}\Data\Daily\Chip'
todayStr = date.today().strftime("%Y%m%d")

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
            return False
            
        soup = BeautifulSoup(resp.text, 'lxml')
        errorMessage = soup.select('#Label_ErrorMsg')[0].get_text()
        print('錯誤訊息: ' + errorMessage)
        
        if not errorMessage: 
            nodes = soup.select('#HyperLink_DownloadCSV')
            if len(nodes) == 0:
                print('任務失敗，沒有下載連結')
                return False
            
            # 下載分點進出 CSV
            resp = session.get(f'{base_url}/bsContent.aspx')
            if resp.status_code != 200:
                print('任務失敗，無法下載分點進出 CSV')
                return False

            #print(resp.text)

            # 寫檔案
            fileContent = resp.text.replace('�W', '')
            Utils.WriteFile(f'{path}\{todayStr}\{stockId}.csv', fileContent)
            
        return True
def GetVolumeIndicator(stockId):
    #print(f'{path}\{stockId}.csv')
    # 讀取檔案, 根據,, 切割字串
    lines = [line.strip().split(",,") for line in open(f'{path}\{todayStr}\{stockId}.csv', 'r')]
    # flat list in list 
    data = reduce(operator.concat, lines)[7:]
    #print(data)
    data = [entry.split(',') for entry in data]
    #print(data)
    df = pd.DataFrame(data, columns=['序號', '券商', '價格', '買進股數', '賣出股數']).dropna()
    df['買進股數'] = df['買進股數'].astype(int)
    df['賣出股數'] = df['賣出股數'].astype(int)
    df.to_csv(f'{path}\{todayStr}\{stockId}_籌碼資料.csv',encoding='utf_8_sig')

    # 刪除檔案
    # 重新命名整理後的檔案
    try:
        os.remove(f'{path}\{todayStr}\{stockId}.csv')
        os.rename(f'{path}\{todayStr}\{stockId}_籌碼資料.csv', f'{path}\{todayStr}\{stockId}.csv')
    except OSError as e:
        print(e)
    #print(df.sort_values('賣出股數', ascending=False).head(15))
    #print(df)
    
    # TOP 1 買超 = 買最多股票的券商 買多少
    top1Buy = df['買進股數'].max()
    # TOP 1 賣超 = 賣最多股票的券商 賣多少
    top1Sell = df['賣出股數'].max()
    # 超額買超 = TOP 1 買超 / TOP 1 賣超
    overBuy = round(top1Buy / top1Sell, 2)
                
    if overBuy > 2.0:
        overBuy = '🏆' + overBuy
    print('top1Buy:' + str(top1Buy) + ', top1Sell:' + str(top1Sell) + ', overBuy:' + str(overBuy));
    
    # 買方的前 15 名買超量 
    top15Buy = df.sort_values('買進股數', ascending=False).head(15)['買進股數'].sum()
    # 賣方的前 15 名賣超量
    top15Sell = df.sort_values('賣出股數', ascending=False).head(15)['賣出股數'].sum()
    # 籌碼集中 = 買方的前 15 名買超量 - 賣方的前 15 名賣超量
    volumeFloat = top15Buy - top15Sell
    #print('top15Buy:' + str(top15Buy) + ', top15Sell:' + str(top15Sell) + ', volumeFloat:' + str(volumeFloat))
    
    # 總成交量
    totalVolume = df['買進股數'].sum()
    # 籌碼集中度(%) = 籌碼集中 ÷ 總成交量
    volumeFloatRate = round(volumeFloat / totalVolume * 100, 2)
    if volumeFloatRate > 20:
        volumeFloatRate = '🏆' + str(volumeFloatRate)
    print('totalVolume:' + str(totalVolume) + ', volumeFloat:' + str(volumeFloat) + ', volumeFloatRate:' + str(volumeFloatRate))

    return pd.DataFrame([[overBuy, volumeFloatRate]], columns=['超額買超', '籌碼集中度'])

def GetVolume(stockId):
    error_count = 0
    max_error_count = 10 #最多10次
    while error_count < max_error_count:
        success = DownloadVolume(stockId)
        try:
            if success:
                return GetVolumeIndicator(stockId)
            else:
                time.sleep(random.randint(1, 5))
                error_count = error_count + 1
                print(f'錯誤次數{error_count}')
                
        except Exception as e:
            print(str(e))


#df = GetVolumeIndicator('8112')
df = GetVolume('1604')
print(df)
