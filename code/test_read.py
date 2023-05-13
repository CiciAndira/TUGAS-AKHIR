import pandas as pd

df = pd.read_csv("dataset/EURUSD_M5_October.csv",sep="\t")
df.rename(columns={'<DATE>': 'date', '<TIME>': 'time','<OPEN>': 'open','<HIGH>': 'high','<LOW>': 'low','<CLOSE>': 'close','<TICKVOL>': 'tickvol','<SPREAD>': 'spread','<VOL>': 'vol'}, inplace=True)
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df = df.drop(columns=['date','time'])
df = df[['datetime','open','high','low','close','tickvol','spread','vol']]

df.to_csv("dataset/predict_data.csv")
print(df)