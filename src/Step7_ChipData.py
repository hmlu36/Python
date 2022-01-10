import numpy as np
import requests
from bs4 import BeautifulSoup
from BrowserUserAgent import GetHeader
import UtilsCaptcha
import json
import os
import time
import random

# 參考 https://gist.github.com/CMingTseng/79447ccb2bb41e4bd8ec36d020fccab9

base_url = 'https://bsr.twse.com.tw/bshtm'


def DownloadChip(stockId):
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
        print(captcha)

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
        print(json.dumps(params, indent=2))
        resp = session.post(f'{base_url}/bsMenu.aspx', data=params, headers=headers)
        if resp.status_code != 200:
            print('任務失敗: %d' % resp.status_code)
            exit(1)

        soup = BeautifulSoup(resp.text, 'lxml')
        nodes = soup.select('#HyperLink_DownloadCSV')
        if len(nodes) == 0:
            print('任務失敗，沒有下載連結')
            exit(1)

        # 下載分點進出 CSV
        resp = session.get(f'{base_url}/bsContent.aspx')
        if resp.status_code != 200:
            print('任務失敗，無法下載分點進出 CSV')
            exit(1)
        # print(resp.text)

        # 寫檔案
        path = f'Data\Daily\Chip'
        # 建立資料夾, 如果資料夾不存在時 
        os.makedirs(path, exist_ok=True)
        with open(path + f'\{stockId}.csv', 'w') as file:
            file.write(resp.text.replace('�W', ''))


def GetChip(stockId):
    error_count = 0
    max_error_count = 5 #最多五次

    while error_count < max_error_count:
        try:
            DownloadChip(stockId)
            #執行成功, 跳出迴圈
            break
        except:
            time.sleep(random.randint(10, 20))
            error_count = error_count + 1
            print(f'錯誤次數{error_count}')
        
GetChip('8112')
