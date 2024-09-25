import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
sns.set(style='dark')

def correlation(data):
    corr = data.select_dtypes([np.number]).corr()
    return corr

def rate_pm25_per_station(data):
    pm25_mean_per_station = data.groupby('station')['PM2.5'].mean().reset_index().sort_values(by='PM2.5', ascending=False)
    return pm25_mean_per_station

def rate_co_per_station(data):
    co_mean_per_station = data.groupby('station')['CO'].mean().reset_index().sort_values(by='CO', ascending=False)
    return co_mean_per_station

def rate_no2_per_station(data):
    no2_mean_per_station = data.groupby('station')['NO2'].mean().reset_index().sort_values(by='NO2', ascending=False)
    return no2_mean_per_station

def rate_pm25_permonth(data):
    monthly_avg_pm25 = data.groupby(['station', 'month'])['PM2.5'].mean().reset_index()
    return monthly_avg_pm25

def plot_rate_pm25_perstation(data, max_value):
    colors = ["red" if v==max_value else "lightgrey" for v in data['PM2.5']]
    plt.figure(figsize=(8,8))
    sns.barplot(y='station', x='PM2.5', data=data, palette=colors)
    plt.title("Rata-rata PM2.5 Per Station Dengan Highlight Nilai Tertinggi")
    plt.xlabel("Rata-rata PM2.5")
    plt.ylabel("Nama Station")
    st.pyplot(plt)

def plot_rate_NO2_perstation(data, max_value):
    colors = ["red" if v==max_value else"lightgrey" for v in data['NO2']]
    plt.figure(figsize=(8,8))
    sns.barplot(y='station', x='NO2', data=data, palette=colors)
    plt.title("Rata-rata NO2 Per Station Dengan Highlight Nilai Tertinggi")
    plt.xlabel("Rata-rata NO2")
    plt.ylabel("Nama Station")
    st.pyplot(plt)

def plot_rate_co_perstation(data, max_value):
    colors = ["red" if v==max_value else"lightgrey" for v in data['CO']]
    plt.figure(figsize=(8,8))
    sns.barplot(y='station', x='CO', data=data, palette=colors)
    plt.title("Rata-rata CO Per Station Dengan Highlight Nilai Tertinggi")
    plt.xlabel("Rata-rata CO")
    plt.ylabel("Nama Station")
    st.pyplot(plt)


def plot_year_pm25(data):
    # Visualisasi menggunakan seaborn
    plt.figure(figsize=(10, 8))
    sns.lineplot(data=data, x='month', y='PM2.5', hue='station', marker='o')
    # Pengaturan visualisasi
    plt.title(f'Rata-rata PM2.5 Bulanan per Kota ({start_date}, {end_date})')
    plt.xlabel('Bulan')
    plt.ylabel('PM2.5 (µg/m³)') 
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.legend(title='Kota')
    st.pyplot(plt)

df = pd.read_csv(r'C:\Users\ASUS\submission\data\df_final.csv')

datetime_col = ["date"]
for column in datetime_col:
    df[column] = pd.to_datetime(df[column])

min_date = df['date'].min()
max_date = df['date'].max()

with st.sidebar:
    st.header("GOODBREATH.COM")

    start_date, end_date = st.date_input(
        label="Rentang Waktu Input",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['date']>= str(start_date)) & 
             (df['date']<= str(end_date))]


rate_co_per_station_df = rate_co_per_station(main_df)
rate_pm25_per_station_df = rate_pm25_per_station(main_df)
rate_no2_per_station_df = rate_no2_per_station(main_df)
rate_pm25_permonth_df = rate_pm25_permonth(main_df)

st.title("Dashboard Air Quality Dataset")

st.header("Visualisasi Linechart")
st.text("Untuk mendapatkan hasil analisis yang optimal, kita perlu memilih rentang waktu selama 1 tahun.")

col1, col2 = st.columns(2)

with col1:
    st.metric(label='Nilai Tertinggi', value=rate_pm25_permonth_df['PM2.5'].max())

with col2:
    st.metric(label='Nilai Terendah', value=rate_pm25_permonth_df['PM2.5'].min())
plot_year_pm25(rate_pm25_permonth_df)

st.subheader("Visualisasi Barchart Rate PM2.5, CO, dan NO2")
tab1, tab2, tab3 = st.tabs([f"Rata-Rata NO2 {start_date} - {end_date}", f"Rata-Rata CO {start_date} - {end_date}", f"Rata-Rata PM2.5 {start_date} - {end_date}"])

with tab1:
     st.metric(label='Nilai Tertinggi', value=rate_no2_per_station_df['NO2'].max())
     max_value_no2 = rate_no2_per_station_df['NO2'].max()
     plot_rate_NO2_perstation(rate_no2_per_station_df, max_value_no2)
     st.text("Dapat dilihat bahwa nilai yang di highlight dengan warna merah merupakan nilai rata-rata tertinggi.")
 
with tab2:
    st.metric(label='Nilai Tertinggi', value=rate_co_per_station_df['CO'].max())
    max_value_co = rate_co_per_station_df['CO'].max()
    plot_rate_co_perstation(rate_co_per_station_df, max_value_co)
    st.text("Dapat dilihat bahwa nilai yang di highlight dengan warna merah merupakan nilai rata-rata tertinggi.")

with tab3:
   st.metric(label='Nilai Tertinggi', value=rate_pm25_permonth_df['PM2.5'].max())
   max_value_pm25 = rate_pm25_per_station_df['PM2.5'].max()
   plot_rate_pm25_perstation(rate_pm25_per_station_df, max_value_pm25)
   st.text("Dapat dilihat bahwa nilai yang di highlight dengan warna merah merupakan nilai rata-rata tertinggi.")


st.subheader("Tabel 5 Data Teratas")
st.table(data=df.head())

st.caption("Copyright By Angga")
    