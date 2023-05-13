from modul.scrap import scrap_realtime
from modul.preprocessing import series_to_supervised



df = scrap_realtime()
df = df.dropna()
df = df[['time','close','open','high','low','ma5','rsi','macd_l','macd_s','tenkan_sen','kijun_sen','chikou_span' ]]
print(df)