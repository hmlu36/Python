import os
import re
import requests
import sys
import json
from bs4 import BeautifulSoup
import UtilsCaptcha

session = requests.Session()
resp = session.get('https://bsr.twse.com.tw/bshtm/bsMenu.aspx')
if resp.status_code == 200:
    soup = BeautifulSoup(resp.text, 'lxml')
    nodes = soup.select('form input')
    params = {}
    for node in nodes:
        name = node.attrs['name']

        # 忽略鉅額交易的 radio button
        if name in ('RadioButton_Excd', 'Button_Reset'):
            continue

        if 'value' in node.attrs:
            params[node.attrs['name']] = node.attrs['value']
        else:
            params[node.attrs['name']] = ''

    # 找 captcha 圖片
    captcha_image = soup.select('#Panel_bshtm img')[0]['src']
    print(captcha_image)
    m = re.search(r'guid=(.+)', captcha_image)
    if m is None:
        exit(1)

    
    img = UtilsCaptcha.GetCaptcha('https://bsr.twse.com.tw/bshtm/' + captcha_image)
    captcha = UtilsCaptcha.DecodeCaptcha(img)
    print(captcha)
    params['CaptchaControl1'] = captcha
    params['TextBox_Stkno'] = '2330'

    # 送出
    print(json.dumps(params, indent=2))
    resp = session.post('https://bsr.twse.com.tw/bshtm/bsMenu.aspx', data=params)
    if resp.status_code != 200:
        print('任務失敗: %d' % resp.status_code)
        exit(1)

    soup = BeautifulSoup(resp.text, 'lxml')
    nodes = soup.select('#HyperLink_DownloadCSV')
    if len(nodes) == 0:
        print('任務失敗，沒有下載連結')
        exit(1)

    # 下載分點進出 CSV
    resp = session.get('https://bsr.twse.com.tw/bshtm/bsContent.aspx')
    if resp.status_code != 200:
        print('任務失敗，無法下載分點進出 CSV')
        exit(1)

    print(resp.text)