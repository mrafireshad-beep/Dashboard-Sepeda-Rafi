import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Menampilkan versi library di sidebar dashboard untuk pengecekan
st.sidebar.divider()
st.sidebar.write("### 🛠️ Sistem Info (Requirements Check):")
st.sidebar.write(f"**Streamlit:** {st.__version__}")
st.sidebar.write(f"**Pandas:** {pd.__version__}")
st.sidebar.write(f"**Matplotlib:** {matplotlib.__version__}")
st.sidebar.write(f"**Seaborn:** {sns.__version__}")
st.sidebar.write(f"**Babel:** {babel.__version__}")

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set(style='dark')

# 1. --- LOAD & PREPROCESSING DATA ---
@st.cache_data # Biar loading data lebih cepat saat ganti filter
def load_data():
    # Sesuaikan path dengan lokasi di laptopmu
    path = r"dashboard/all_data_daily_processed.csv"
    df = pd.read_csv(path)
    
    # Konversi tanggal
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Pastikan kolom waktu tersedia untuk filter
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month_name()
    
    # Mapping Musim (Jika belum ada di CSV)
    seasons_map = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    if 'season_label' not in df.columns:
        df['season_label'] = df['season'].map(seasons_map)
        
    # Imputasi missing value sederhana jika ada
    if 'demand_level' in df.columns:
        df['demand_level'] = df['demand_level'].fillna(df['demand_level'].mode()[0])
    
    return df

df = load_data()

# 2. --- SIDEBAR FILTER ---
st.sidebar.header('Filter Dashboard 📊')

# Filter Tahun
selected_years = st.sidebar.multiselect(
    'Pilih Tahun',
    options=df['year'].unique().tolist(),
    default=df['year'].unique().tolist()
)

# Filter Bulan (Urutan Kalender)
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
selected_months = st.sidebar.multiselect(
    'Pilih Bulan',
    options=month_order,
    default=month_order
)

# Filter Musim
selected_seasons = st.sidebar.multiselect(
    'Pilih Musim',
    options=df['season_label'].unique().tolist(),
    default=df['season_label'].unique().tolist()
)

# Apply Filter
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['month'].isin(selected_months)) &
    (df['season_label'].isin(selected_seasons))
]

# 3. --- DASHBOARD MAIN PAGE ---
st.title('Analisis Peminjaman Sepeda Harian 🚴‍♀️')

if not filtered_df.empty:
    # --- Metrik Utama ---
    col1, col2, col3 = st.columns(3)
    with col1:
        total_rentals = filtered_df['cnt'].sum()
        st.metric('Total Peminjaman', f'{total_rentals:,}')
    with col2:
        avg_rentals = filtered_df['cnt'].mean()
        st.metric('Rata-rata Harian', f'{avg_rentals:,.0f}')
    with col3:
        reg_ratio = (filtered_df['registered'].sum() / filtered_df['cnt'].sum()) * 100
        st.metric('Persentase Registered', f'{reg_ratio:.1f}%')

    st.divider()

    # --- Visualisasi 1: Tren ---
    st.subheader('📈 Tren Peminjaman Sepeda')
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.lineplot(x='dteday', y='cnt', data=filtered_df, ax=ax, color='#2471A3')
    ax.set_title('Fluktuasi Peminjaman per Hari', fontsize=15)
    st.pyplot(fig)

    # --- Visualisasi 2 & 3: Perbandingan ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader('🌤️ Berdasarkan Kondisi Cuaca')
        fig2, ax2 = plt.subplots()
        # Menggunakan kolom weathersit_label jika ada, jika tidak pakai weathersit asli
        weather_col = 'weathersit_label' if 'weathersit_label' in filtered_df.columns else 'weathersit'
        sns.barplot(x=weather_col, y='cnt', data=filtered_df, ax=ax2, palette='viridis')
        st.pyplot(fig2)

    with col_right:
        st.subheader('👥 Proporsi Tipe Pengguna')
        total_cas = filtered_df['casual'].sum()
        total_reg = filtered_df['registered'].sum()
        fig3, ax3 = plt.subplots()
        ax3.pie([total_cas, total_reg], labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=['#F1948A', '#85C1E9'], startangle=90)
        st.pyplot(fig3)

else:
    st.error("Data tidak ditemukan untuk filter tersebut. Silakan sesuaikan filter Anda.")

# Footer
st.caption('Copyright (c) 2024 - Muhammad Rafi R F')
