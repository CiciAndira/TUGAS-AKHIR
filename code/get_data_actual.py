from modul.scrap import scrap_date
from modul.preprocessing import series_to_supervised
from modul.preprocessing import append_list_as_row

import pytz
from datetime import datetime
from datetime import timedelta

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
datetime_data = datetime(2022, 7, 1, 0, 0, 0,tzinfo=timezone) + timedelta(days=1)# format (yyyy, mm, dd, hh, mm, ss)

df = scrap_date(datetime_data)
df = df.dropna()
df = df[['time','close' ]]

print(df.tail(5))

df.to_csv("result/actual.csv")