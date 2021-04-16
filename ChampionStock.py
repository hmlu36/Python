import time
import datetime
import pandas as pd
import numpy as np
import requests
from Models.settings import db
from pony.orm import *
from functools import reduce

import Utils.dailyExchangeReport as exchange
import Utils.sma as sma
'''
選股條件：
一．基本面
    （１）評估價值是否被低估？（股票價格不會太貴）
        １．本益比　　　　　　　　　　　　　　　＜１５倍
        ２．現金殖利率　　　　　　　　　　　　　＞　５％
    （２）確定本業利益是成長的，且為本業賺的（不是靠業外收益賺的，獲利不持久）
        １．營收累計年增率　　　　　　　　　　　＞　０％
        ２．毛利率　　　　　　　　　　　　　　　＞　０％
        ３．營業利益率　　　　　　　　　　　　　＞　０％
        ４．稅前淨利率　　　　　　　　　　　　　＞　０％
        ５．稅後淨利率　　　　　　　　　　　　　＞　０％
        ６．本業收益（營業利益率／稅前淨利率）　＞６０％
    （３）確定配息不是虛假的．（營運現金流有賺錢，才可以配股息）
        １．近一年（２０１７）營運現金流　　　　＞０
        ２．近一季（２０１８Ｑ３）營運現金流　　＞０
    以上確定選出來的股票是低本益比＋高殖利率，未避免條件過於嚴格，所以先由寬至嚴，若標準太低，導致選出來的股票較多，可以把條件設嚴格．
二．技術面（這是確定底部打好，且已經向上，不摸底）
    １．股價　＞　均線ＭＡ１０
    ２．股價　＞　均線ＭＡ２０
    ３．均線ＭＡ１０　與　均線ＭＡ２０　呈現黃金交叉
三．籌碼面
    １．董監持股　＞　１０％以上
    ２．法人持續買超天數　＞　２天
    董監持股高，對於公司有信心
    三大法人持續買超二天以上，至少短時間看好
'''

# 基本面
dailyExchange_df = exchange.GetDailyExchange()
# 本益比(Price-to-Earning Ratio)
PE = pd.to_numeric(dailyExchange_df['本益比'], errors='coerce') < 15
# 殖利率(Dividend yield)
DY = pd.to_numeric(dailyExchange_df['殖利率(%)'], errors='coerce') > 5
# 淨價比(Price-to-Book Ratio) 找到股價淨值比小於0.7的股票
PBR = pd.to_numeric(dailyExchange_df['股價淨值比'], errors='coerce') <= 1.81
candidate = dailyExchange_df[(PE & DY & PBR)]
# print(candidate)

with db_session:
    rows = db.select(
        "           StockInfo.stockId                                                  " +
        "         , name                                                               " +
        "         , industry                                                           " +
        "         , yearSeason                                                         " +
        "         , revenue                                                            " +
        "         , profitAfterTax                                                     " +
        "         , grossMargin                                                        " +
        "         , operatingIncome                                                    " +
        "         , profitAfterTaxPercentage                                           " +
        "         , roe                                                                " +
        "         , eps                                                                " +
        "         , cashDividends                                                      " +
        "         , stockDividends                                                     " +
        "         , totalDividends                                                     " +
        "      from StockInfo                                                          " +
        "      join StockDetail                                                        " +
        "        on StockInfo.stockId = StockDetail.stockId                            " +
        " left join StockDividend                                                      " +
        "        on StockInfo.stockId = StockDividend.stockId                          " +
        "       and StockDividend.year = (select max(year) from StockDividend temp     " +
        "                                  where StockDividend.stockId = temp.stockId) " +
        "    where yearSeason in (select max(yearSeason) from StockDetail temp         " +
        "                          where temp.stockId = StockDetail.stockId)           " +
        "      and StockInfo.stockId in ('" + "','".join(candidate['證券代號']) + "')   " +
        "      and grossMargin > 0                                                     " +
        "      and operatingIncome > 0                                                 " +
        "      and profitAfterTaxPercentage > 0                                        " +
        "      and revenue > 0                                                         " +
        "      and operatingIncome > profitAfterTaxPercentage                          " +
        "      and roe > 10                                                            " +
        "      and eps > StockDividend.totalDividends                                  " +
        "     and (select count(*) from StockDividend temp                             " +
        "           where StockInfo.stockId = temp.stockId) > 5                        " +
        " order by StockInfo.stockId;                                                  ")[:]
    # print(rows)
    data = []
    for row in rows:
        data.append([row.stockId, row.name, row.industry, row.yearSeason, row.revenue, row.profitAfterTax, row.grossMargin,
                    row.operatingIncome, row.profitAfterTaxPercentage, row.roe, row.eps, row.cashDividends, row.stockDividends, row.totalDividends])

    merge_df = pd.DataFrame(rows, columns=[["證券代號", "證券名稱", "產業別", "年/季", "營收(億)",
                                            "稅後淨利(億)", "毛利(%)", "營業利益(%)", "稅後淨利(%)", "ROE(%)", "EPS(%)", "現金股利", "股票股利", "合計股利"]])
    print(merge_df)
    # print(merge_df['證券代號'])

 


# df = reduce(lambda dailyExchange_df, stockInfo_df: pd.merge(dailyExchange_df, stockInfo_df, on=['證券代號', '證券名稱']), [dailyExchange_df, stockInfo_df])
# print(df)
