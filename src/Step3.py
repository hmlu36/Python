import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import random

'''
1. 營收累計年增率 > ０％
2. 毛利率 > ０％
3. 營業益益率 > ０％
4. 稅前淨利率 > ０％
5. 稅後淨利率 > ０％
6. 本業收益（營業利益率／稅前淨利率） > ６０％
'''
def GetPageContent(url):
    print(url)

    # 要睡覺一下，不然會被ben掉
    time.sleep(random.randint(0, 10))

    rawData = requests.get(url)
    rawData.encoding = 'big5'
    #print(rawData.text)
    #print(rawData.encoding) # 網頁encoding
    soup = BeautifulSoup(rawData.text, "html.parser")
    getdata = ""
    if soup.find('font') is None or soup.find('font').text != '檔案不存在!':
        print("content exists")
        getdata = pd.read_html(url)
    #print(getdata)
    return getdata
        

def IncomeFilter(stockId):
    ### 現在時間處裡 ###
    now = datetime.datetime.now()  # 現在的時間
    year = now.strftime("%Y")  # 抓今年
    lastmonth = now - datetime.timedelta(days=31)  # 一個月前的時間

    for season in range(4, 0, -1):
        print('stockId:' + stockId)
        print('season:' + str(season))

        ### 先與網站請求抓到每天的報價資料 ###
        url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + stockId + '&SYEAR=' + year + '&SSEASON=' + str(season) + '&REPORT_ID=C'
        getdata = GetPageContent(url)

        '''
        if getdata == "":
            url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + stockId + '&SYEAR=' + str(int(year)-1) + '&SSEASON=4&REPORT_ID=C'
            getdata = GetPageContent(url)

        if getdata == "":
            url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=' + stockId + '&SYEAR=' + str(int(year)-1) + '&SSEASON=3&REPORT_ID=C'
        
        '''
        if getdata == "":
            continue

        del getdata[0]  # 殺掉第一個，因為第一個沒有意義
        print(getdata[0]['會計項目Accounting Title']);


        # 營收要比去年高
        if getdata[1][getdata[1]['會計項目'] == '營業收入合計'].values[0][3] > getdata[1][getdata[1]['會計項目'] == '營業收入合計'].values[0][4]:
            # 毛利跟營收要是正的
            if getdata[1][getdata[1]['會計項目'] == '營業收入合計'].values[0][3] > 0 and getdata[1][getdata[1]['會計項目'] == '營業毛利（毛損）淨額'].values[0][3] > 0:
                # 營業利益是正的
                if getdata[1][getdata[1]['會計項目'] == '營業利益（損失）'].values[0][3] > 0:
                    # 稅前稅後淨利是正的
                    if getdata[1][getdata[1]['會計項目'] == '繼續營業單位稅前淨利（淨損）'].values[0][3] > 0 and getdata[1][getdata[1]['會計項目'] == '繼續營業單位本期淨利（淨損）'].values[0][3] > 0:
                        # 本業收益（營業利益率／稅前淨利率）　＞６０％
                        if (getdata[1][getdata[1]['會計項目'] == '營業利益（損失）'].values[0][3]/getdata[1][getdata[1]['會計項目'] == '營業收入合計'].values[0][3])/(getdata[1][getdata[1]['會計項目'] == '繼續營業單位稅前淨利（淨損）'].values[0][3]/getdata[1][getdata[1]['會計項目'] == '營業收入合計'].values[0][3]) > 0.6:
                            # 營運現金是正的>0
                            if getdata[2][getdata[2]['會計項目'] == '本期現金及約當現金增加（減少）數'].values[0][1] > 0 and getdata[2][getdata[2]['會計項目'] == '本期現金及約當現金增加（減少）數'].values[0][2] > 0:

                                # 檢查價格超過MA10、MA20
                                avgprice = []
                                url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=' + \
                                    now.strftime("%Y%m%d") + \
                                    '&stockNo=' + stockId

                                # 要睡覺一下，不然會被ben掉
                                time.sleep(random.randint(0, 10))

                                list_req = requests.get(url)  # 請求網站
                                soup = BeautifulSoup(
                                    list_req.content, "html.parser")  # 將整個網站的程式碼爬下來
                                jsonsoup = json.loads(str(soup))
                                for i in range(len(jsonsoup['data'])-1):
                                    avgprice.append(
                                        float(jsonsoup['data'][i][1]))

                                # 如果不夠20日，就爬上個月的價格
                                if len(avgprice) < 19:
                                    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=' + \
                                        lastmonth.strftime(
                                            "%Y%m%d") + '&stockNo=' + stockId

                                    # 要睡覺一下，不然會被ben掉
                                    time.sleep(random.randint(0, 10))

                                    list_req = requests.get(url)  # 請求網站
                                    soup = BeautifulSoup(
                                        list_req.content, "html.parser")  # 將整個網站的程式碼爬下來
                                    jsonsoup = json.loads(str(soup))
                                    for i in range(len(jsonsoup['data'])-1, 1, -1):
                                        avgprice.append(
                                            float(jsonsoup['data'][i][1]))
                                # 計算出平均並且進行判斷
                                avg20 = sum(avgprice[:20])/20
                                
                                # ------------------------------先顯示目前價格----------------------------------
                                # 要抓取的網址
                                url = 'https://tw.stock.yahoo.com/q/q?s=' + stockId
                                # 請求網站
                                list_req = requests.get(url)
                                # 將整個網站的程式碼爬下來
                                soup = BeautifulSoup(list_req.content, "html.parser")
                                # 找到b這個標籤
                                get_stock_price = soup.findAll('b')[1].text  # 裡面所有文字內容
                                if avg20 < float(get_stock_price):
                                    avg10 = sum(avgprice[:10])/10
                                    if avg10 < float(get_stock_price):
                                        # 黃金交叉
                                        if avg20 < avg10:
                                            # 檢查董監事持股比例
                                            data = {
                                                'step': '1',
                                                'firstin': '1',
                                                'off': '1',
                                                'queryName': 'co_id',
                                                'inpuType': 'co_id',
                                                'TYPEK': 'all',
                                                'isnew': 'true',
                                                'co_id': stockId
                                            }

                                            headers = {
                                                'Host': 'mops.twse.com.tw',
                                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                                            }

                                            url = 'http://mops.twse.com.tw/mops/web/stapap1'
                                            list_req = requests.post(
                                                url, data=data, headers=headers)
                                            soup = BeautifulSoup(
                                                list_req.content, "html.parser")
                                            stockbroad = soup.find_all(
                                                'td', {'style': 'text-align:right !important;'})
                                            if int(stockbroad[-2:-1][0].text.replace(' ', '').replace(',', ''))/getdata[3][getdata[3]['Unnamed: 0'] == '期末餘額'].values[0][2] > 0.1:

                                                # 檢查三大法人買賣狀況
                                                countstock = 0
                                                sumstock = 0
                                                for i in range(5, 0, -1):
                                                    date = datetime.datetime.strftime(
                                                        datetime.datetime.now() - datetime.timedelta(days=i), '%Y%m%d')
                                                    r = requests.get(
                                                        'https://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999')
                                                    if r.text != '\r\n':  # 有可能會沒有爬到東西，有可能是六日
                                                        countstock += 1
                                                        get = pd.read_csv(StringIO(r.text), header=1).dropna(
                                                            how='all', axis=1).dropna(how='any')
                                                        # 找到我們要搜尋的股票
                                                        get = get[get['證券代號']
                                                                == stockId]
                                                        if len(get) > 0:
                                                            get['三大法人買賣超股數'] = get['三大法人買賣超股數'].str.replace(
                                                                ',', '').astype(float)
                                                            if get['三大法人買賣超股數'].values[0] > 0:
                                                                sumstock += 1

                                                if countstock == sumstock:
                                                    candidate2.append(stockId)




IncomeFilter("2330")