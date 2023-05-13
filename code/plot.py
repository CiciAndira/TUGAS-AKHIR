import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt


def mape(actual, pred):
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs((actual - pred) / actual)) * 100


def rmse(actual, pred):
    return sqrt(mean_squared_error(actual, pred))


data = pd.read_csv('result-22012023-230754.csv')
print(data)

actualData = data['Actual']
# print(f"Actual Data: {actualData}")
predictData = data['Predict'].astype(float)
# print(f"Predict Data: {predictData}")
mape_value = mape(actualData, predictData)
rmse_value = rmse(actualData, predictData)

fig = plt.figure(figsize=(10, 5))
plt.plot(data['Time'], data['Actual'], label='actual')
plt.plot(data['Time'], data['Predict'], label='predict')
plt.legend()
plt.show()