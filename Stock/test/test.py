import twstock
stock = twstock.Stock('1474')
#stock.fetch(2021, 3)
print(stock.price)
bfp = twstock.BestFourPoint(stock)
print(bfp.best_four_point_to_buy()) # 判斷是否為四大買點
print(bfp.best_four_point_to_sell())  # 判斷是否為四大賣點
print(bfp.best_four_point())          # 綜合判斷