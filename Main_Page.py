import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="SPK Mahasiswa Teladan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "data_sampel.csv")
    df = pd.read_csv(file_path)
    return df.sample(300, random_state=42)

df = load_data()

st.title("🎓 SPK Pemilihan Mahasiswa Teladan")
st.subheader("Berbasis Logika Fuzzy Mamdani")
st.markdown("---")

st.markdown("""
Penilaian mahasiswa teladan di lingkungan akademik pada umumnya masih sangat bergantung pada 
satu indikator tunggal, yaitu nilai pencapaian akademik (GPA). Padahal, mahasiswa yang ideal 
tidak hanya unggul secara akademis, tetapi juga mampu menjaga keseimbangan hidup.

Faktor-faktor seperti keaktifan berorganisasi, gaya hidup sehat, manajemen waktu digital, 
dan kesehatan mental juga tak kalah penting, namun seringkali diabaikan karena sulit diukur 
secara matematis pasti.

Sistem ini menggunakan **Logika Fuzzy Mamdani** untuk merepresentasikan ketidakpastian 
penilaian tersebut secara lebih adil dan menyeluruh.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Data Explorer")
    st.markdown("""
    Eksplorasi dataset mahasiswa secara interaktif. 
    Lihat distribusi variabel, hubungan antar faktor, 
    dan filter data sesuai kebutuhan.
    """)

with col2:
    st.markdown("### 🧮 SPK Fuzzy")
    st.markdown("""
    Lihat fungsi keanggotaan setiap variabel, 
    simulasikan skor individu, dan jalankan 
    perangkingan seluruh dataset.
    """)

with col3:
    st.markdown("### 👤 Profil")
    st.markdown("""
    Informasi kelompok pengembang sistem, 
    pembagian tugas, dan referensi proyek.
    """)

st.markdown("---")

st.markdown("### Ringkasan Dataset")

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Total Data", len(df))
col_b.metric("Jumlah Jurusan", df["major"].nunique())
col_c.metric("Jumlah Negara", df["country"].nunique())
col_d.metric("Rata-rata GPA", f"{df['GPA'].mean():.2f}")

st.markdown("---")
st.markdown("### Preview Dataset")
st.caption("300 baris data acak dari dataset global university students performance.")
st.dataframe(df, use_container_width=True, height=400)

st.markdown("---")
st.caption("Dibuat untuk memenuhi Proyek Akhir Praktikum SCPK 2025/2026 · Program Studi Informatika · UPN Veteran Yogyakarta")