import datetime
import pandas as pd

last_date="2023-09-20"

list_new_dates=[]

for i in range(100):
    x=pd.to_datetime(last_date)+datetime.timedelta(days=i)
    list_new_dates.append(x.strftime("%Y-%m-%d"))

print(list_new_dates)