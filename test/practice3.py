import pandas as pd

rank_url = 'https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=TAI&n=100'
print(rank_url)
html_tables = pd.read_html(rank_url, encoding='utf8')
print(len(html_tables)) # 頁面中有幾組 <table></table> 標記