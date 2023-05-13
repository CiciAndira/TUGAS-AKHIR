from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import LSTM
from matplotlib import pyplot
from numpy import concatenate

from modul.scrap import scrap_date
from modul.preprocessing import series_to_supervised
from modul.preprocessing import append_list_as_row

from sklearn.metrics import mean_squared_error
from math import sqrt
from datetime import timedelta
from datetime import datetime

import pandas as pd
from pandas import DataFrame
import pytz

currency = "EURUSD"
interval = "5m"
len_data = "1000"

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
datetime_data = datetime(2022, 7, 1, 0, 0, 0, tzinfo=timezone)  # format (yyyy, mm, dd, hh, mm, ss)
i = 0
while i < 500:
    datetime_data = datetime_data + timedelta(minutes=5)
    df = scrap_date(datetime_data)
    df = df.dropna()
    df = df[['time', 'close', 'open', 'high', 'low', 'ma5', 'rsi', 'macd_l', 'macd_s', 'tenkan_sen', 'kijun_sen',
             'chikou_span']]

    # remove realtime data doesnt valid
    # df = df[:-1]

    dataset = df
    dataset = dataset.set_index('time')

    predict_data = dataset.tail(1)

    time_predict_data = predict_data.index.values[0]
    time_predict_data = pd.to_datetime(time_predict_data) + timedelta(minutes=5)

    predict_data = predict_data.values
    predict_data = predict_data.astype('float32')

    values = dataset.values
    values = values.astype('float32')
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    scaled_predict = scaler.transform(predict_data)

    # frame as supervised learning
    reframed = series_to_supervised(scaled, 1, 1)
    reframed = reframed.iloc[:, 0:(len(dataset.columns) + 1)]
    print(reframed)
    scaled_predict = DataFrame(scaled_predict)
    # print(scaled_predict)
    scaled_predict.columns = reframed.columns[range(0, (len(dataset.columns)))]

    # split into train and test sets
    values = reframed.values
    n_train_hours = 800
    train = values[:n_train_hours, :]
    test = values[n_train_hours:, :]
    # split into input and outputs
    train_X, train_y = train[:, :-1], train[:, -1]
    test_X, test_y = test[:, :-1], test[:, -1]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

    values_predict = scaled_predict.values
    predict_data_x = values_predict.reshape((values_predict.shape[0], 1, values_predict.shape[1]))

    print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

    model = load_model("model/EURUSD")
    history = model.fit(train_X, train_y, epochs=100, batch_size=32, validation_data=(test_X, test_y), verbose=1,
                        shuffle=False)
    model.save("model/EURUSD")
    # pyplot.plot(history.history['loss'], label='train')
    # pyplot.plot(history.history['val_loss'], label='test')
    # pyplot.legend()
    # pyplot.show()

    # make a prediction
    yhat_predict = model.predict(predict_data_x)
    print(predict_data_x)
    # predict_data_x
    predict_data_x_new = predict_data_x.reshape((predict_data_x.shape[0], predict_data_x.shape[2]))

    inv_yhat_predict_new = concatenate((yhat_predict, predict_data_x_new[:, 1:]), axis=1)
    inv_yhat_predict_new = scaler.inverse_transform(inv_yhat_predict_new)
    inv_yhat_predict_new = inv_yhat_predict_new[:, 0]
    print(time_predict_data)
    print("%.10f" % inv_yhat_predict_new[0])

    row_contents = [time_predict_data, inv_yhat_predict_new[0]]
    # Append a list as new line to an old csv file
    append_list_as_row('result/predict.csv', row_contents)
