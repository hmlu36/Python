
import numpy as np
from fake_useragent import UserAgent

# 建立虛擬的Header User agent清單,防止IP被鎖。可用fake-useragent套件創建隨機user agent
ua = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
      'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
      'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36']

referer = [
    'https://sherry-freedomlifestyle.com/beginners-guide-to-financial-statements/',
    'https://jerrywangtc.blog/2020/05/10/stock-website/',
    'https://george-dewi.com/financial-stock-deposit/',
    'https://enjoyfreedomlife.com/how-to-choose-stocks/',
    'https://enjoyfreedomlife.com/how-to-use-b-band/',
    'https://jerrywangtc.blog/2020/12/21/stock-website-app/',
    'https://www.storm.mg/article/2960261',
    'https://foremostgroups.com.tw/',
    'https://slides.com/marconi_jiang/stock',
    'https://earning.tw/stock-saving-recommend/',
    'https://pig-school.com/who-is-eps/',
    'https://www.dcard.tw/f/money/p/229998959',
    'https://www.pupuliao.info/',
    'https://www.wearn.com/bbs/t964908.html',
    'https://www.life.tw/?app=view&no=911331',
    'https://igoamazing.com/python-selenium/',
    'https://retireearly.com.tw/what-is-eps/',
    'https://shop.nstock.tw/author/article?id=184',
    'https://valueinmind.co/zh/blog/investment/etf-investment-for-newbies/',
    'https://wowgaopei.com/fundamental/',
    'https://www.google.com/'
]


def GetHeader():
    return {'user-agent': UserAgent().random, 'Referer': referer[np.random.randint(0, len(referer))]}


# data = GetHeader()
# print(data)
