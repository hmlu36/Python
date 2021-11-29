import matplotlib.pyplot as plt
import pandas as pd
import twstock

''' 
    參考
    https://pixnashpython.pixnet.net/blog/post/43244764
    https://ithelp.ithome.com.tw/articles/10205113
'''

# 這是抓取歷史資料
twstock.__update_codes()
stock = twstock.Stock('2069')
print(stock.price[0])
price = stock.price[-5:]       # 近五日之收盤價
high = stock.high[-5:]         # 近五日之盤中高點
low = stock.low[-5:]           # 近五日之盤中低點
date = stock.date[-5:]         # 近五日的日期
close = stock.price[-5:]       # 近五日的收盤

print('price--->', price)
print('high--->', high)
print('low--->', low)
print('close--->', close)
print('date--->', date)


print(stock.moving_average(stock.price, 5)) #5日平均價格
print(stock.moving_average(stock.capacity, 5))
print(stock.ma_bias_ratio(5, 10))


bfp = twstock.BestFourPoint(stock)
print(bfp.best_four_point_to_buy())   # 判斷是否為四大買點
print(bfp.best_four_point_to_sell())  # 判斷是否為四大賣點
print(bfp.best_four_point())          # 綜合判斷
'''
o 量大收紅 / 量大收黑
o 量縮價不跌 / 量縮價跌
o 三日均價由下往上 / 三日均價由上往下
o 三日均價大於六日均價 / 三日均價小於六日均價
'''