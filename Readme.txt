# Forex prediction
PEMANFAATAN DATA TEKNIKAL UNTUK MEMPREDIKSI NILAI TUKAR MATA UANG MENGGUNAKAN METODE PATTERN RECOGNITION

## Disclaimers
Sistem prediksi menggunakan metode Deep Learning yang merupakan bagian dari Neural Network yaitu Long Short Term Memory (LSTM). 
Sistem prediksi yang dirancang menggunakan nilai tukar mata uang EUR/USD dengan time frame 5m.
Sistem prediksi ini memanfaatkan data indikator teknikal yang terdiri dari 
moving average (MA), ichimoku kinko hyo, relative strength index (RSI), 
moving average convergence divergence (MACD), dan stochastic. 

## Installation
untuk menjalankan proyek, berikut yang harus diinstal
1. Metatrader, app ini berguna untuk mendownload data dimana data tersebut digunakan sebagai masukkan sistem sebelum melakukan prediksi
2. Visual studio code, app ini berguna untuk menjalankan/ membuka sistem prediksi nilai tukar mata uang

## Running the Project
1. Download data dimetatrader untuk masukkan sistem (tidak ada syarat berapa data kebelakang yang harus diambil)
2. Buka visual studio code untuk membuka file main.py 
3. Jalankan file main.py dengan "streamlit run main.py" sistem prediksi akan tertampil dan melakukan prediksi dengan data yang sudah didownload sebelumnya 