import requests
import re
import pandas as pd
from BbrowserUserAgent import GetHeader

#proxy_json = pd.read_json(url);


valid_ips = []
for page in range(1,10):
    response = requests.get(f"https://proxylist.geonode.com/api/proxy-list?limit=200&page={page}&sort_by=lastChecked&sort_type=desc&filterLastChecked=50&protocols=http%2Chttps%2Csocks4%2Csocks5")
    proxy_json = response.json()
    #print(proxy_json['data'])
    
    for proxy in proxy_json['data']:
        #print(proxy)
        #print(proxy['ip'])
        try:
            result = requests.get('https://ip.seeip.org/jsonip?', proxies={'http': proxy['ip'] + ':' + proxy['port'], 'https': proxy['ip'] + ':' + proxy['port']}, timeout=5)
            print(result.json())
            valid_ips.append(proxy['ip'] + ':' + proxy['port'])
        except:
            print(f"{proxy['ip'] + ':' + proxy['port']} invalid")

print(valid_ips)
'''
for proxy in range(len(proxy_json['data'])):
    print(proxy)
    print(proxy['ip'])
    try:
        result = requests.get('https://ip.seeip.org/jsonip?', proxies={'http': proxy['ip'], 'https': proxy['ip']}, timeout=5)
        print(result.json())
        valid_ips.append(proxy['ip'])
    except:
        print(f"{proxy['ip']} invalid")
		
with open('proxy_list.txt', 'w') as file:
    for ip in valid_ips:
        file.write(ip + '\n')
    file.close()
'''
'''
#url = "https://www.sslproxies.org/"
response = requests.get(url)
    
proxy_ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', response.text)  #「\d+」代表數字一個位數以上
print(proxy_ips)

valid_ips = []
for ip in proxy_ips:
    try:
        result = requests.get('https://ip.seeip.org/jsonip?', proxies={'http': ip, 'https': ip}, timeout=5)
        print(result.json())
        valid_ips.append(ip)
    except:
        print(f"{ip} invalid")
		
with open('proxy_list.txt', 'w') as file:
    for ip in valid_ips:
        file.write(ip + '\n')
    file.close()
'''