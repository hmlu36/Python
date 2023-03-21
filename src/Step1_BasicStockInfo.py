import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import re
from lxml import etree
from decimal import Decimal
from datetime import datetime, timedelta
import os
from datetime import date
import pyuser_agent
import ssl
import Utils
from Step11_GetNetWorth import GetNetWorth

# 發現是urlopen https時需要驗證一次SSL證書，當網站目標使用自簽名的證書時就會跳出這個錯誤
ssl._create_default_https_context = ssl._create_unverified_context

# 本益比, 淨值比
def GetDailyExchangeReport(filter):
    # ----------------- （１）評估價值是否被低估？（股票價格不會太貴） -------------
    ########## 去公開資訊觀測站，把本益比、股價淨值比爬下來 ##########
    url = f"https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=&selectType=&_={str(time.time())}"
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson = json.loads(soup.text)

    # 因為是表格式，用dataframe處理會比較方便
    stockdf = pd.DataFrame(getjson["data"], columns=["證券代號", "證券名稱", "殖利率(%)", "股利年度", "本益比", "股價淨值比", "財報年/季"])

    del stockdf["財報年/季"]
    del stockdf["股利年度"]

    stockdf = stockdf.rename(columns={"殖利率(%)": "殖利率", "股價淨值比": "淨值比"})

    if filter:
        # errors = 'coerce'：是因為本益比千位數有逗號，若改成value會出錯，這個指令是讓出錯的地方以NaN型式取代
        # 找到股價淨值比小於0.7的股票
        PBR = pd.to_numeric(stockdf["淨值比"], errors="coerce") < 0.8
        PER = pd.to_numeric(stockdf["本益比"], errors="coerce") < 10  # 找到本益比小於10的股票
        DividendYield = pd.to_numeric(stockdf["殖利率"].replace("-", 0), errors="coerce") > 3  # 殖利率 > 3

        candidate = stockdf[(PER & DividendYield)]  # 綜合以上兩者，選出兩者皆符合的股票
        # print(candidate)
        return candidate
    else:
        return stockdf


# 取出每日收盤價
def GetDailyExchange():
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&type=ALLBUT0999"
    jsonData = requests.get(url).json()
    # print(jsonData)
    df = pd.DataFrame(jsonData["data9"], columns=jsonData["fields9"])
    df = df[["證券代號", "收盤價"]]
    return df


# 資本額
def GetStockCapital(filter):
    df = pd.read_csv("https://mopsfin.twse.com.tw/opendata/t187ap03_L.csv")
    # print(df)

    if filter:
        # 大於等於5年的上市公司
        fiveYearBefore = (datetime.today() - timedelta(days=5 * 365)).strftime("%Y%m%d")
        # print(fiveYearBefore)
        YEAR_CONDITION = pd.to_datetime(df["上市日期"], format="%Y%m%d") < fiveYearBefore
        df = df[YEAR_CONDITION]

    # data = df.set_index("公司代號")["上市日期"].to_dict()
    df[["公司代號", "成立日期", "上市日期"]] = df[["公司代號", "成立日期", "上市日期"]].astype(str)
    # rename dataframe specific column name
    # ref: https://stackoverflow.com/questions/20868394/changing-a-specific-column-name-in-pandas-dataframe
    df["實收資本額"] = pd.to_numeric(df["實收資本額"], downcast="float") / 100000000
    return df[["公司代號", "公司名稱", "實收資本額", "成立日期", "上市日期"]].rename(columns={"公司代號": "證券代號", "實收資本額": "資本額"})
    # print(data)
    # return data

# 營利率
def GetOperatingMargin():
    df = GetFinancialStatement('營益分析')
    df.columns = ["證券代號", "公司名稱", "營業收入", "毛利率", "營業利益率", "稅前純益率", "稅後純益率"]
    # df['營業收入'] = df['營業收入'].astype(float) / 100
    del df["公司名稱"]
    
    df["營業收入"] = pd.to_numeric(df["營業收入"], downcast="float") / 100
    return df

def GetBasicStockInfo(filter=False):

    exchangeReport = GetDailyExchangeReport(filter)
    
    capital = GetStockCapital(filter)
    

    # merge dataframe
    # ref: http://violin-tao.blogspot.com/2017/06/pandas-2-concat-merge.html
    merge_df = pd.merge(capital, exchangeReport, on="證券代號")
    #print(merge_df)

    if filter:
        operatingMargin_df = GetOperatingMargin()
        merge_df = pd.merge(merge_df, operatingMargin_df, on="證券代號")
        # print(merge_df)

        dailyExhange_df = GetDailyExchange()
        merge_df = pd.merge(merge_df, dailyExhange_df, on="證券代號")
        
        #netWorth_df = GetNetWorth()
        #merge_df = pd.merge(merge_df, netWorth_df, on="證券代號")

        # 董監持股比例
        #directShareHold_df = pd.read_csv(f"{GetRootPath()}\Data\Monthly\董監持股比例.csv")
        #directShareHold_df = directShareHold_df.rename(columns={"代號": "證券代號", "全體  董監  持股  (%)": "全體董監持股(%)"})
        ## print(directShareHold_df)
        #directShareHold_df = directShareHold_df[["證券代號", "全體董監持股(%)"]].astype(str)
        directShareHold_df = GetDirectorSharehold()
        merge_df = pd.merge(merge_df, directShareHold_df, on="證券代號")
        
        # 股東分布資料
        shareHoder_df = GetAllShareholderDistribution()
        shareHoder_df["100-1000張人數"] = shareHoder_df[["101-200張人數", "201-400張人數", "401-800張人數", "801-1000張人數"]].sum(axis=1)
        shareHoder_df["100-1000張比例"] = shareHoder_df[["101-200張人數", "201-400張人數", "401-800張人數", "801-1000張人數"]].sum(axis=1)
        shareHoder_df = shareHoder_df[["證券代號", "100張以下人數", "100張以下比例", "100-1000張人數", "100-1000張比例", "1000張以上人數", "1000張以上比例"]].astype(str)
        merge_df = pd.merge(merge_df, shareHoder_df, on="證券代號")
        
    # move column in pandas dataframe
    # ref https://stackoverflow.com/questions/35321812/move-column-in-pandas-dataframe
    column_to_move = merge_df.pop("證券名稱")
    merge_df.insert(1, "證券名稱", column_to_move)
    # print(merge_df)
    merge_df.to_csv(f"{Utils.GetRootPath()}\Data\Temp\基本資訊.csv", encoding="utf_8_sig")
    return merge_df


'''
https://www.finlab.tw/python-%E8%B2%A1%E5%A0%B1%E7%88%AC%E8%9F%B2-1-%E7%B6%9C%E5%90%88%E6%90%8D%E7%9B%8A%E8%A1%A8/
'''
def GetFinancialStatement(type='綜合損益'):
    # 判斷是哪個年度第幾季
    # 參考: https://www.nstock.tw/author/article?id=184
    now = date.today()
    current_year = now.year
    roc_year = current_year - 1911
    season = 0

    last_q4_day = date(current_year, 3, 31)  # 前一年度第四季
    q1_day = date(current_year, 5, 15)  # 第一季(Q1)財報：5/15前
    q2_day = date(current_year, 8, 14)  # 第二季(Q2)財報：8/14前
    q3_day = date(current_year, 11, 14)  # 第三季(Q3)財報：11/14前
    q4_day = date(current_year + 1, 3, 31)  # 第四季(Q4)財報及年報：隔年3/31前

    if now <= last_q4_day:
        roc_year -= 1
        season = 3
    elif now <= q1_day and now > last_q4_day:
        roc_year -= 1
        season = 4
    elif now <= q2_day and now > q1_day:
        season = 1
    elif now <= q3_day and now > q2_day:
        season = 2
    elif now <= q4_day and now > q3_day:
        season = 3

        
    if type == '綜合損益':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')

    form_data = {
        "encodeURIComponent": 1,
        "step": 1,
        "firstin": 1,
        "off": 1,
        "TYPEK": "sii",
        "year": roc_year,
        "season": season,
    }

    response = requests.post(url, form_data)
    response.encoding = "utf8"

    soup = BeautifulSoup(response.text, "html.parser")
    # print(response.text)
    # df = translate_dataFrame(response.text)
    if not soup.find(string=re.compile("查詢無資料")):
        df_table = pd.read_html(response.text)
        df = df_table[0]
        #print(df)
        # df.columns = df.columns.get_level_values(0)
        # 刪除重複, 保留唯一的第一列
        df = df.drop_duplicates(keep='first', inplace=False)
        # 將第一列指定為header
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        # 將第三列開只轉為數值
        for col in  df.columns[2:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df[["公司代號"]].rename(columns={"公司代號": "證券代號"})
        #print(df)
        return df

    return pd.DataFrame()


# 股東分布人數
def GetAllShareholderDistribution():
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

    print(s)
    #s.to_csv(f'{GetRootPath()}\Data\Weekly\股東分布資料.csv',encoding='utf_8_sig')
    return s

# 董監事持股比
def GetDirectorSharehold():
    # 取自神秘金字塔
    url = "https://norway.twsthr.info/StockBoardTop.aspx"
    cssSelector = "#details"
    df = GetDataFrameByCssSelector(url, cssSelector)
    df.columns = df.columns.get_level_values(0)
    
    #print(df)
    #擷取所需欄位
    df = df.iloc[:, [3, 7]] 
    
    df['證券代號'] = df['個股代號/名稱'].str[0:4]
    df['公司名稱'] = df['個股代號/名稱'].str[4:]
    df = df[['證券代號', '持股比率 %']]
    df = df.rename(columns={"持股比率 %": "全體董監持股(%)"})
    return df

# ------ 共用的 function ------
# 根目錄路徑
def GetRootPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def GetDataFrameByCssSelector(url, css_selector):
    #ua = fake_useragent.UserAgent()
    ua = pyuser_agent.UA()
    user_agent = ua.random
    headers = {"user-agent": user_agent}
    rawData = requests.get(url, headers=headers, timeout=(5, 10)) 
    #Max 5 seconds to connect to server and max 10 seconds to wait on response
    
    rawData.encoding = "utf-8"
    soup = BeautifulSoup(rawData.text, "html.parser")
    data = soup.select_one(css_selector)
    try:
        dfs = pd.read_html(data.prettify())
    except:
        return pd.DataFrame()

    # print(dfs)
    if len(dfs[0]) > 1:
        return dfs[0]
    if len(dfs[1]) > 1:
        return dfs[1]
    return dfs

# ------ 測試 ------
print(GetBasicStockInfo(True))
#print(GetDirectorSharehold())
