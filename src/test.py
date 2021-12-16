
import random
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime, timedelta

print(UserAgent().random)
print(random.randint(15, 60))
print((datetime.today() - timedelta(days=5 * 365)).strftime('%Y%m%d'))