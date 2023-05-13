import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from modul.scrap import scrap_csv
from predict_csv import mape, rmse, predict

# ---- PARAMETER ---- #
rasio = 0.9
epoch = 50
batch_size = 128
neuron = 100
# ---- PARAMETER ---- #

ext = ['csv']
current_datetime = datetime.now().strftime("%d%m%Y-%H%M%S")

dirs = os.getcwd()
template_csv = pd.DataFrame(columns=['Time', 'Actual', 'Predict'])
df_result = template_csv.copy()

result_csv = os.path.join(dirs, f'result-{current_datetime}.csv')


@st.cache
def convert_df(dataframe):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')


st.set_page_config(
    layout='wide',
    page_title="Sistem Prediksi Nilai Tukar Mata Uang"
)

st.markdown("<h1 style='text-align: center; '>Sistem Prediksi Nilai Tukar Mata Uang</h1>", unsafe_allow_html=True)
st.markdown("")

col1, _ = st.columns([1, 1])
col3, col4, col5, _ = st.columns([3, 1, 1, 1])

with col3:
    uploadDisable = False
    files = st.file_uploader(
        "Insert File (.csv)",
        accept_multiple_files=False,
        type=ext,
        disabled=uploadDisable)

with col5:
    st.markdown('')
    st.markdown('')
    st.markdown('')

col21, col22, col23, col24, col25 = st.columns([1, 1, 1, 1, 1])
col211, col221, col231, col241, col251 = st.columns([1, 1, 1, 1, 1])






# with col21:
#     st.markdown("<h6 style='text-align: center; "
#                 "background-color: #262631; "
#                 "padding-top: 10px;"
#                 "padding-bottom: 10px'>Aktual</h5>", unsafe_allow_html=True)
#     # with st.expander("Tabel Aktual"):
#     placeholderTable1 = st.empty()
#     if files is None:
#         df_temp = template_csv
#         df_temp['Time'] = pd.to_datetime(df_temp['Time'], format="%Y-%m-%d %H:%M:%S")
#         placeholderTable1.table(df_temp[["Time", "Actual"]])
#     else:
#         df_result = df_result
#         df_result['Time'] = pd.to_datetime(df_result['Time'], format="%Y-%m-%d %H:%M:%S")
#         placeholderTable1.table(df_result[["Time", "Actual"]])

# with col22:
#     st.markdown("<h6 style='text-align: center; "
#                 "background-color: #262631; "
#                 "padding-top: 10px;"
#                 "padding-bottom: 10px'>Prediksi</h5>", unsafe_allow_html=True)

#     # with st.expander("Tabel Prediksi"):
#     placeholderTable2 = st.empty()
#     if files is None:
#         df_temp = template_csv
#         df_temp['Time'] = pd.to_datetime(df_temp['Time'], format="%Y-%m-%d %H:%M:%S")
#         placeholderTable2.table(df_temp[["Time", "Predict"]])
#     else:
#         df_result = df_result
#         df_result['Time'] = pd.to_datetime(df_result['Time'], format="%Y-%m-%d %H:%M:%S")
#         placeholderTable2.table(df_result[["Time", "Predict"]])

if files is not None:
    
    df = scrap_csv(files)
    

    # ------------------------Looping-------------------------------
    # for i in range(start, end):
    # waktu, act, pred = predict(df, start)
    # new_row = {
    #     "Time": waktu,
    #     "Actual": act,
    #     "Predict": pred
    # }
    # df_result = df_result.append(new_row, ignore_index=True)
    # df_result.to_csv(result_csv, index=False)
    # df_result['Time'] = pd.to_datetime(df_result['Time'], format="%Y-%m-%d %H:%M:%S")
    # placeholderTable1.table(df_result[["Time", "Actual"]])
    # placeholderTable2.table(df_result[["Time", "Predict"]])

    timePredict, pricePredict = predict(df, rasio, epoch, batch_size, neuron)
    data = df.tail(4).reset_index()

    for i in range(4):
        with globals()[f'col2{i+1}']:
            st.text("Actual")
            globals()[f'txtArea{i+1}'] = st.empty()
            d = ""
            dc = 'off'
            if i != 0:
                if (data['close'][i] > data['close'][i-1]):
                    d = "Uptrend"
                    dc = "normal"
                else:
                    d = "- Downtrend"
                    dc = "normal"
            
            globals()[f'txtArea{i+1}'].metric(str(data['time'][i]), f"%.5f" % data['close'][i], delta=d, delta_color=dc)
    
    with col25:
        st.text("Predict")
        txtArea5 = st.empty()
        
        if (float(pricePredict) > data['close'][3]):            
            txtArea5.metric(str(timePredict), pricePredict, delta="Uptrend", delta_color="normal")
        else:
            txtArea5.metric(str(timePredict), pricePredict, delta="- Downtrend", delta_color="normal")



    # data = pd.read_csv(result_csv)
    # data['Time'] = pd.to_datetime(data['Time'], format="%Y-%m-%d %H:%M:%S")
    # _, col31, _ = st.columns([1, 2, 1])
    # with col31:
    #     csv = convert_df(data)
    #     st.download_button(
    #         label="Download Result as CSV",
    #         data=csv,
    #         file_name=result_csv,
    #         mime='text/csv'
    #     )

    # actualData = data['Actual']
    # predictData = data['Predict'].astype(float)
    # mape_value = mape(actualData, predictData)
    # rmse_value = rmse(actualData, predictData)

    # st.title("EURUSD Timeframe 5m \nRMSE : %.3f \nMAPE : %.3f" % (rmse_value, mape_value))
    # fig = plt.figure(figsize=(10, 5))
    # plt.plot(data['Time'], data['Actual'], label='actual')
    # plt.plot(data['Time'], data['Predict'], label='predict')
    # plt.legend()
    # st.pyplot(fig)
