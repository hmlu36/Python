import yahoo_price as yp
stock_list = ['2330', '2317', '2324']

for stockId in stock_list:
    price = yp.stock_price(stockId + ".TW")
    print('股票:', stockId, '| 價格:', price)