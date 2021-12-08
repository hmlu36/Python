# -*-coding:utf-8 -*-
import io
import sys

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
except:
    pass

import requests
import re
import time
from lxml import etree

UrlCompanyInfo = 'https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='
UrlCompanyDividend = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID='
UrlCompanyProfit = 'https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# 抓取ID公司名稱與產業別


def Get_Company_Info(strID):
    resInfo = requests.get(UrlCompanyInfo+strID, headers=headers)
    resInfo.encoding = 'utf-8'
    htmlInfo = etree.HTML(resInfo.text)

    XpathCompanyName = '/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[2]/tbody/tr[1]/td[2]'
    CompanyName = htmlInfo.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathCompanyName) + '/text()')[0]

    XpathCompanyIndustry = '/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]/table[2]/tbody/tr[2]/td[2]'
    CompanyIndustry = htmlInfo.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathCompanyIndustry) + '/text()')[0]
    print(CompanyName)
    print(CompanyIndustry)


# 抓取股利政策
def Get_Company_Dividend(strID):
    resDividend = requests.get(UrlCompanyDividend+strID, headers=headers)
    resDividend.encoding = 'utf-8'
    text = resDividend.text
    text = text.replace('<nobr>', '').replace('</nobr>', '')
    text = text.replace('<br>', '\n')
    text = text.replace('<b>', '').replace('</b>', '')
    htmlDividend = etree.HTML(text)

    XpathDividendHeader1 = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/thead[1]/tr[1]/td'
    liNode = htmlDividend.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathDividendHeader1))
    cols = 0
    for node in liNode:
        if node.attrib.has_key('colspan'):
            cols += int(node.attrib['colspan'])
        else:
            cols += 1

    liHeader = [['']*cols for i in range(4)]

    i = 0
    for node in liNode:
        rows = 1
        if node.attrib.has_key('rowspan'):
            rows = int(node.attrib['rowspan'])

        cols = 1
        if node.attrib.has_key('colspan'):
            cols = int(node.attrib['colspan'])

        for col in range(cols):
            for row in range(rows):
                liHeader[row][col+i] = node.text.replace('\u3000', '').replace(
                    '\xa0', '').replace('\n', '').replace(' ', '')
        i += cols

    XpathDividendHeader = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/thead[1]/tr'
    trs = htmlDividend.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathDividendHeader))
    r = 0
    c = 0
    for tr in trs:
        if r != 0:
            for td in tr.getchildren():
                rows = 1
                if td.attrib.has_key('rowspan'):
                    rows = int(td.attrib['rowspan'])

                cols = 1
                if td.attrib.has_key('colspan'):
                    cols = int(td.attrib['colspan'])

                for col in range(cols):
                    for row in range(rows):
                        while liHeader[row+r][col+c] != '':
                            c += 1
                        liHeader[row+r][col+c] = td.text.replace('\u3000', '').replace(
                            '\xa0', '').replace('\n', '').replace(' ', '')
                c += cols
        r += 1
        c = 0

    # 設定想要的欄位內容
    liDividend = [
        ['股利發放年度',
         '合計', '合計', '股利合計',  # 股利
         '最高', '最低', '年均',  # 股價
         '現金', '股票', '合計', 'EPS(元)',  # 殖利率
         '配息', '配股', '合計',  # 發放率
         ]
    ]

    # 找出欄位索引值
    colData = [0]*len(liDividend[0])
    for i in range(len(colData)):
        if i > 0:
            colData[i] = liHeader[3].index(liDividend[0][i], colData[i-1])
        else:
            colData[i] = liHeader[3].index(liDividend[0][i])

    XpathDividendData = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/tbody[1]/tr'
    trs = htmlDividend.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathDividendData))

    for tr in trs:
        li = ['']*len(liDividend[0])
        i = 0
        tds = tr.getchildren()
        for i in range(len(li)):
            li[i] = tds[colData[i]].text
            if li[i] == None or li[i] == '-':
                li[i] = ''

        liDividend.append(li)
    return liDividend


# 抓取獲利狀況
def Get_Company_Profit(strID):
    resProfit = requests.get(UrlCompanyProfit+IdCompany, headers=headers)
    resProfit.encoding = 'utf-8'
    text = resProfit.text
    text = text.replace('<nobr>', '').replace('</nobr>', '')
    text = text.replace('<br>', '\n')
    text = text.replace('<b>', '').replace('</b>', '')
    htmlProfit = etree.HTML(text)

    XpathProfitHeader1 = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/thead[1]/tr[1]/td'
    liNode = htmlProfit.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathProfitHeader1))
    cols = 0
    for node in liNode:
        if node.attrib.has_key('colspan'):
            cols += int(node.attrib['colspan'])
        else:
            cols += 1

    liHeader = [['']*cols for i in range(4)]

    i = 0
    for node in liNode:
        rows = 1
        if node.attrib.has_key('rowspan'):
            rows = int(node.attrib['rowspan'])

        cols = 1
        if node.attrib.has_key('colspan'):
            cols = int(node.attrib['colspan'])

        for col in range(cols):
            for row in range(rows):
                liHeader[row][col+i] = node.text.replace('\u3000', '').replace(
                    '\xa0', '').replace('\n', '').replace(' ', '')
        i += cols

    XpathProfitHeader = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/thead[1]/tr'
    trs = htmlProfit.xpath(
        re.sub(r'/tbody([[]\\d[]])?', '', XpathProfitHeader))
    r = 0
    c = 0
    for tr in trs:
        if r != 0:
            for td in tr.getchildren():
                rows = 1
                if td.attrib.has_key('rowspan'):
                    rows = int(td.attrib['rowspan'])

                cols = 1
                if td.attrib.has_key('colspan'):
                    cols = int(td.attrib['colspan'])

                for col in range(cols):
                    for row in range(rows):
                        while liHeader[row+r][col+c] != '':
                            c += 1
                        liHeader[row+r][col+c] = td.text.replace('\u3000', '').replace(
                            '\xa0', '').replace('\n', '').replace(' ', '')
                c += cols
        r += 1
        c = 0

    # 設定想要的欄位內容
    liProfit = [
        ['年度', '財報評分',
         '收盤', '平均', '漲跌', '漲跌(%)',  # 股價
         '營業收入', '營業毛利', '稅後淨利',  # 獲利金額
         '營業毛利', '稅後淨利',  # 獲利率
         'ROE(%)', '稅後EPS', '年增(元)'
         ]
    ]

    # 找出欄位索引值
    colData = [0]*len(liProfit[0])
    for i in range(len(colData)):
        if i > 0:
            colData[i] = liHeader[1].index(liProfit[0][i], colData[i-1])
        else:
            colData[i] = liHeader[1].index(liProfit[0][i])

    XpathProfitData = '/html/body/table[2]/tbody/tr/td[3]/div[2]/div/div/table/tbody[1]/tr'
    trs = htmlProfit.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XpathProfitData))

    for tr in trs:
        li = ['']*len(liProfit[0])
        i = 0
        tds = tr.getchildren()
        for i in range(len(li)):
            if len(tds[colData[i]].getchildren()) == 0:
                li[i] = tds[colData[i]].text
            else:
                li[i] = tds[colData[i]].getchildren()[0].text

            if li[i] == None or li[i] == '-':
                li[i] = ''

        liProfit.append(li)
    return liProfit


def Sleep_And_Print(sec):
    for i in range(1, sec+1):
        time.sleep(1)
        print(i, end=' ')
    print('')


IdCompany = '2330'
Get_Company_Info(IdCompany)
# Sleep_And_Print(15)
#liDividend = Get_Company_Dividend(IdCompany)
# for i in range(len(liDividend)):
#    print(liDividend[i])
# Sleep_And_Print(15)
'''
liProfit = Get_Company_Profit(IdCompany)
for i in range(len(liProfit)):
    print(liProfit[i])
'''