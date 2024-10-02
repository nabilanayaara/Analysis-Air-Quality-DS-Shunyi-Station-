import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 

# Fungsi untuk memuat data dari file CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk membersihkan data dari missing values dan kolom tidak diperlukan
def clean_data(df):
    # Menghapus baris yang memiliki nilai null
    df_cleaned = df.dropna()
    
    # Mengonversi kolom 'year', 'month', 'day', 'hour' menjadi datetime
    if all(col in df_cleaned.columns for col in ['year', 'month', 'day', 'hour']):
        df_cleaned['date'] = pd.to_datetime(df_cleaned[['year', 'month', 'day', 'hour']])
    elif 'date' in df_cleaned.columns:
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
    
    # Menghapus kolom yang tidak diperlukan
    df_cleaned = df_cleaned.drop(columns=['No'], errors='ignore')
    return df_cleaned

# Menampilkan informasi dasar dan deskriptif dataset
def display_info(df):
    st.subheader("Data Awal:")
    st.write(df.head())
    
    st.subheader("Informasi Dasar Dataset:")
    st.write(df.info())
    
    st.subheader("Missing Values:")
    st.write(df.isnull().sum())
    
    st.subheader("Statistik Deskriptif:")
    st.write(df.describe())
    
    st.subheader("Data Duplikat:")
    st.write(df.duplicated().sum())

# Visualisasi scatter plot antara PM2.5 dan variabel lingkungan
def plot_scatter(df_cleaned):
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))
    
    # Subplot 1: Hubungan antara PM2.5 dan Suhu (TEMP)
    sns.scatterplot(x='TEMP', y='PM2.5', data=df_cleaned, ax=ax[0])
    ax[0].set_title('Hubungan PM2.5 dan Suhu')
    ax[0].set_xlabel('Suhu (TEMP)')
    ax[0].set_ylabel('Konsentrasi PM2.5')
    
    # Subplot 2: Hubungan antara PM2.5 dan Kelembaban (DEWP)
    sns.scatterplot(x='DEWP', y='PM2.5', data=df_cleaned, ax=ax[1])
    ax[1].set_title('Hubungan PM2.5 dan Kelembaban')
    ax[1].set_xlabel('Kelembaban (DEWP)')
    ax[1].set_ylabel('Konsentrasi PM2.5')
    
    # Subplot 3: Hubungan antara PM2.5 dan Kecepatan Angin (WSPM)
    sns.scatterplot(x='WSPM', y='PM2.5', data=df_cleaned, ax=ax[2])
    ax[2].set_title('Hubungan PM2.5 dan Kecepatan Angin')
    ax[2].set_xlabel('Kecepatan Angin (WSPM)')
    ax[2].set_ylabel('Konsentrasi PM2.5')
    
    plt.tight_layout()
    st.pyplot(fig)

# Visualisasi pola bulanan dari PM2.5 dan PM10
def plot_monthly_pattern(df_cleaned):
    # Mengelompokkan data berdasarkan bulan, kemudian menghitung rata-rata PM2.5 dan PM10
    monthly_avg = df_cleaned.groupby('month')[['PM2.5', 'PM10']].mean().reset_index()
    
    # Visualisasi Pola Bulanan dari PM2.5 dan PM10
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_avg, x='month', y='PM2.5', marker='o', label='PM2.5')
    sns.lineplot(data=monthly_avg, x='month', y='PM10', marker='o', color='orange', label='PM10')
    
    plt.title('Pola Bulanan dari PM2.5 dan PM10')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Konsentrasi')
    plt.legend(title='Konsentrasi')
    plt.tight_layout()
    st.pyplot(plt)

# Visualisasi pola tahunan dari PM2.5 dan PM10
def plot_annual_pattern(df_cleaned):
    # Mengelompokkan data berdasarkan tahun dan bulan, kemudian menghitung rata-rata PM2.5 dan PM10
    monthly_avg = df_cleaned.groupby(['year', 'month'])[['PM2.5', 'PM10']].mean().reset_index()
    
    # Membuat kolom 'date' untuk visualisasi
    monthly_avg['date'] = pd.to_datetime(monthly_avg[['year', 'month']].assign(day=1))
    
    # Visualisasi Pola Tahunan dan Musiman dari PM2.5 dan PM10
    fig, ax = plt.subplots(2, 1, figsize=(14, 7))
    
    # Plot PM2.5
    sns.lineplot(data=monthly_avg, x='date', y='PM2.5', marker='o', ax=ax[0])
    ax[0].set_title('Pola Tahunan dan Musiman dari PM2.5')
    ax[0].set_xlabel('Tanggal')
    ax[0].set_ylabel('Rata-rata PM2.5')
    
    # Plot PM10
    sns.lineplot(data=monthly_avg, x='date', y='PM10', marker='o', color='orange', ax=ax[1])
    ax[1].set_title('Pola Tahunan dan Musiman dari PM10')
    ax[1].set_xlabel('Tanggal')
    ax[1].set_ylabel('Rata-rata PM10')
    
    plt.tight_layout()
    st.pyplot(fig)

# Fungsi utama untuk menjalankan kode
def main():
    st.title("Visualisasi Data PM2.5 dan PM10")

    # Upload file CSV
    uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
    
    if uploaded_file is not None:
        # Memuat data
        shunyi_data = load_data(uploaded_file)
        st.success("Data berhasil dimuat!")
        
        # Tampilkan informasi data
        display_info(shunyi_data)
        
        # Bersihkan data
        shunyi_cleaned = clean_data(shunyi_data)
        
        # Plot visualisasi
        st.subheader("Visualisasi Scatter Plot:")
        plot_scatter(shunyi_cleaned)
        
        st.subheader("Pola Bulanan dari PM2.5 dan PM10:")
        plot_monthly_pattern(shunyi_cleaned)
        
        st.subheader("Pola Tahunan dan Musiman dari PM2.5 dan PM10:")
        plot_annual_pattern(shunyi_cleaned)

# Menjalankan aplikasi
if __name__ == "__main__":
    main()
