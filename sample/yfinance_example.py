import yfinance as yf

stock = yf.Ticker("2330.TW")

# 歷史股價紀錄(起訖區間)
#df = stock.history(start="2022-01-01", end="2022-12-12")

# 歷史股價紀錄(起訖最大區間)
#df = stock.history(period="max")

#股票基本信息
#df_info = stock.info
#print(df_info)

# 內部人士與機構法人持有比例
#major_holders = stock.major_holders
#print(major_holders)

# 主要持有的法人機構
#ins_holders = stock.institutional_holders
#print(ins_holders)

# 損益表
#fin_data = stock.financials
#print(fin_data)

# 資產負債表
#balance_data = stock.balance_sheet
#print(balance_data)

#現金流量表
#cf_data = stock.cashflow
#print(cf_data)

#分析師建議
print(stock.recommendations)