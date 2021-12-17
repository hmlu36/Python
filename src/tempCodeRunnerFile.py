import pandas as pd
from decimal import Decimal
import Utils

'''
1. 營收累計年增率 > 0 %
2. 毛利率 > 0 %
3. 營業利益率 > 0 %
4. 稅前淨利率 > 0 %
5. 稅後淨利率 > 0 %
6. 本業收益（營業利益率／稅前淨利率） > 60 %
7. ROE > 10 %
8. 董監持股比例 > 20
'''      

def GetFinHeaders():
    return ['毛利率', '營業利益率', '股東權益報酬率(年預估)', '稅前淨利率', '稅後淨利率', '本業收益', '每股營業現金流量', '每股自由現金流量']

def GetFinDetail(stockId):
    url = f"https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID={stockId}"
    df = Utils.GetDataFrameByClass(url, 'b1 p4_4 r0_10 row_mouse_over');
    #print(df)
    data = {}

    headers = GetFinHeaders()
    for header in headers:
        if header == '本業收益':
             #本業收益（營業利益率／稅前淨利率） > ６０％
            tempData = round(Decimal(data['營業利益率']) / Decimal(data['稅前淨利率']) * 100, 2)
            data.update({'本業收益': str(tempData)})
        else:
            tempData = Utils.GetDataFrameValueByLabel(df, '獲利能力', header)
            data.update({header: str(Decimal(tempData[0]))})
    print(list(data.keys()))
    print(list(data.values()))
    df = pd.DataFrame(data.items())
    return df

# 測試
data = GetFinDetail("8112")
print(data)
