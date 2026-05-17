import streamlit as st

st.set_page_config(
    page_title="Mahasiswa Teladan",
    initial_sidebar_state="collapsed",
)

st.title("Sistem Pendukung Keputusan Pemilihan Mahasiswa Teladan")
st.markdown("---")
st.info("""
**Daftar menu:**
1. Data Explorer: Eksplorasi dan visualisasi data mentah mahasiswa
2. SPK Fuzzy: Menghitung skor teladan dan perankingan mahasiswa
3. Profil Developer 
""")

st.markdown("---")
st.caption("Dibuat untuk memenuhi tugas akhir Praktikum SCPK")