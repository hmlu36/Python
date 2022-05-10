import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import time
from io import StringIO
import random
import requests
import re
from lxml import etree
from decimal import Decimal
from datetime import datetime, timedelta
import os
import Utils


# 取出每日收盤價
def GetDailyExchange():
    url = 'https://www.twse.com.tw/fund/BFI82U?response=csv&dayDate=20220509&weekDate=20220509&monthDate=20220509&type=day'
    jsonData = requests.get(url).json()
    #print(jsonData)
    df = pd.DataFrame(jsonData["data9"], columns=jsonData["fields9"])
    df = df[['證券代號', '收盤價']]
    return df