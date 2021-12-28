# coding: utf-8

import shutil
import requests
import re
import csv
import os
import timer
import pytesseract
from PIL import Image
import UtilsCaptcha

#參考 https://github.com/Pregaine/stock/blob/master/01_Day%20process/%E5%88%B8%E5%95%86%E5%88%86%E9%BB%9E/%E6%8D%89%E5%8F%96%E5%8D%B7%E5%95%86%E8%B2%B7%E8%B3%A3.py
# https://ithelp.ithome.com.tw/articles/10227263

#------------------------------------------------------------------------
#網頁頭參數
#詢問得到以下參數
#viewstate, eventvalidation,
#------------------------------------------------------------------------
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0.1) Gecko/2010010' \
    '1 Firefox/4.0.1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-us,en;q=0.5',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}

rs = requests.session()

res = rs.get( 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx', stream = True, verify = False, headers =headers )


viewstate = re.search( 'VIEWSTATE"\s+value=.*=', res.text )
viewstate = viewstate.group( )[18:]

eventvalidation = re.search( 'EVENTVALIDATION"\s+value=.*\w', res.text )
eventvalidation = eventvalidation.group()[24:]

# encode_viewstate = urllib.parse.urlencode( { viewstate : '' }  )
# print( encode_viewstate[:-1] )
# encode_eventvalidation = urllib.parse.urlencode( { eventvalidation : '' } )
# print( encode_eventvalidation[:-1] )
#------------------------------------------------------------------------

#------------------------------------------------------------------------
#搜尋網頁回應內容關鍵字'CaptchaImage.*guid+\S*\w'
#根據關鍵字獲得驗證碼圖片
#------------------------------------------------------------------------
str = re.search( 'CaptchaImage.*guid+\S*\w', res.text ).group( )

res = rs.get( 'http://bsr.twse.com.tw/bshtm/' + str, stream = True, verify = False )

f = open( 'check.png', 'wb' )
shutil.copyfileobj( res.raw, f )
f.close

# print( 'http://bsr.twse.com.tw/bshtm/' + str )
#------------------------------------------------------------------------

#------------------------------------------------------------------------
#初始化參數
#------------------------------------------------------------------------
num = 0
headers = {'User-Agent': 'Mozilla/5.0'}
timeout_dict = dict( )
resort  = 0
#------------------------------------------------------------------------


#------------------------------------------------------------------------
#根據股號清單,詢問網頁
#------------------------------------------------------------------------

rs = requests.session( )

res = rs.get( 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx', stream = True, verify = False, headers = headers, timeout=None )

print( '股號', '8112', 'Response', res.status_code )

#----------------------------------------------------------------------------------
#根據網頁響應內容"res.text"
#取出參數viewstate, eventvalidation
#----------------------------------------------------------------------------------
try:
    viewstate = re.search( 'VIEWSTATE"\s+value=.*=', res.text )
    viewstate = viewstate.group()[18:]
    eventvalidation = re.search( 'EVENTVALIDATION"\s+value=.*\w', res.text )
    eventvalidation = eventvalidation.group( )[ 24: ]
except:
    print('error')
#----------------------------------------------------------------------------------
#根據網頁響應內容"res.text"
#根據參數viewstate, eventvalidation
#得到個股卷商交易資料"date"
#----------------------------------------------------------------------------------
img_url = re.search('CaptchaImage.*guid+\S*\w', res.text)
#print(img_url)

captcha = UtilsCaptcha.clean_captcha(UtilsCaptcha.request_captcha(img_url))
print (pytesseract.image_to_string(captcha).upper())
