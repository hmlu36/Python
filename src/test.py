import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

def crawler(StockID):
  options = Options()
  options.add_argument("--headless")

  url = 'https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID={}&CHT_CAT2=DATE'.format(StockID)

  driver = webdriver.Chrome(options=options)
  driver.get(url)
  sleep(5)
  canvas = driver.find_element_by_css_selector('#StockCanvas')
  canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
  canvas_png = base64.b64decode(canvas_base64)

  with open(r"{}.png".format(StockID), 'wb') as f:
      f.write(canvas_png)
  driver.close()

crawler('1515')