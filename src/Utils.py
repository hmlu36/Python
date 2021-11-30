import re
from datetime import datetime

def GetDataByXPath(htmlInfo, XPath):
    return htmlInfo.xpath(re.sub(r'/tbody([[]\\d[]])?', '', XPath) + '/text()')[0]
    

def GetYearBetween(startDateStr, endDate=datetime.today()):
    date_format = "%Y%m%d"
    startDate = datetime.strptime(str(startDateStr), date_format)
    delta = endDate - startDate
    years = round(delta.days / 365)
    #print(years)
    return years
