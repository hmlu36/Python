import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import UtilsCaptcha
from PIL import Image
from io import BytesIO

def GetChip(stockId):
    base_url = 'http://bsr.twse.com.tw/bshtm/'
    page = requests.get(base_url + 'bsMenu.aspx')
    
    # Get the capthca on TWSE's website. It's the second image on the page.
    soup = BeautifulSoup(page.content, 'html.parser')
    img_url = soup.findAll('img')[1]['src']
    
    url = base_url + img_url
    image = UtilsCaptcha.request_captcha(url)
    captcha = UtilsCaptcha.clean_captcha(image)
    print(captcha)

GetChip('8150')