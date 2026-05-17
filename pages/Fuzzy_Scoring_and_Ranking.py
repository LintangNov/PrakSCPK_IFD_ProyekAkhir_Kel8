import streamlit as st
import pandas as pd
from fuzzy_engine import rank, single_inference
import os

st.title("Perhitungan Skor Teladan dengan Fuzzy")
data_path = os.path.join('data', 'data_sampel.csv')
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    st.error("Sumber dataset tidak ditemukan")
    df = None

@st.cache_data
def run_ranking(dataframe): 
    return rank(dataframe)

# ini ntar kalo mau dihapus gapapa 
if st.button("Jalankan Perangkingan"):
    with st.spinner("Menghitung dan Merangking Skor Fuzzy..."):
        result = run_ranking(df)
        st.dataframe(result)
