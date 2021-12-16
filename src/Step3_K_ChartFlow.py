import pandas as pd
import Utils
import re
'''
抓取本益比
取得現今EPS、本益比、近五年六個級距本益比

選股條件：
1. 本益比小於10
2. 小於近五年最小級距本益比
'''
def GetPE(stockId):

    url = f"https://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stockId}&CHT_CAT=WEEK"
    df = Utils.GetDataFrameByClass(url, 'b1 p4_0 r0_10 row_bg_2n row_mouse_over')
    #firtRowDf = df[df.columns[-5:]].head(1)

    # 取前兩列後面倒數6欄資料
    firtRowDf = df.iloc[0,-6:]
    #print(firtRowDf)

    #dataframe轉成dictionary 參考 https://stackoverflow.com/questions/45452935/pandas-how-to-get-series-to-dict
    data = [dict(key=re.findall(r'[0-9]+[.]?[0-9]*', str(k))[0], value=v) for k, v in firtRowDf.items()]
    #print(data)
    return data


# 測試
data = GetPE("8112")
print(data)
