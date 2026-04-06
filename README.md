# Bike Sharing Data Analysis Dashboard 🚴‍♀️

Dashboard Streamlit ini dibuat untuk memvisualisasikan hasil analisis data dari dataset Bike Sharing. Proyek ini merupakan bagian dari tugas analisis data Dicoding.

## Struktur Direktori
- **/dashboard**: Berisi file utama `dashboard.py` dan dataset yang telah diproses `all_data.csv`.
- **/data**: Berisi dataset mentah (raw data).
- `notebook.ipynb`: File analisis data awal (EDA).
- `requirements.txt`: Daftar library Python yang dibutuhkan.

## Cara Menjalankan Dashboard

### 1. Setup Environment - Anaconda
Jika Anda menggunakan Conda, jalankan perintah berikut:
```bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt

### 2. Masuk ke direktori proyek
cd proyek_analisis_data

# Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
.\venv\Scripts\activate   # Untuk Windows

# Instal library
pip install -r requirements.txt

### 3. Jalankan Aplikasi Streamlit
# Jika Anda berada di root folder proyek
streamlit run dashboard/dashboard.py