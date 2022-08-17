
import requests
import re

# TGOS 取得圖台狀態
# 取得 pagekey 與 session 值
def tgos_get_state():
    print('取得圖台狀態')

	# pagekey 取得途徑: window.sircMessage.sircPAGEKEY = '...';
    r = requests.post('https://map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map.aspx')
    if r.status_code == 200:
        m = re.search('window\.sircMessage\.sircPAGEKEY\s?=\s?\'([\w\+%]+)\';', r.text)
        if m != None:
            cookies = {}
            pagekey = m.group(1)
        for c in r.cookies:
            cookies[c.name] = c.value
        
        print('pagekey:' + pagekey)
        print('sid:' + cookies['ASP.NET_SessionId'])
            
        form_data = {
			'pagekey': pagekey,
            'method':'querymoiaddr',
            'address':'台南市東區東門路三段253號',
            'useoddeven': False,
            'sid': cookies['ASP.NET_SessionId']
        }
        headers =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Accept": "*/*",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "referrer": "https://map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map.aspx?addr=%E5%8F%B0%E5%8D%97%E5%B8%82%E6%9D%B1%E5%8D%80%E6%9D%B1%E9%96%80%E8%B7%AF%E4%B8%89%E6%AE%B5253%E8%99%9F"
        }
        result = requests.post(f'https://map.tgos.tw/TGOSCloud/Generic/Project/GHTGOSViewer_Map.ashx?pagekey={pagekey}', form_data, headers=headers)    
        print(result.text)
            
    else:
        print('無法取得 pagekey')
   
   
   
tgos_get_state()