import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Mahasiswa Teladan",
    initial_sidebar_state="expanded",
)

st.title("Sistem Pendukung Keputusan Pemilihan Mahasiswa Teladan")
st.markdown("---")
st.info("""
**Daftar menu:**
1. Data Explorer: Eksplorasi dan visualisasi data mentah mahasiswa
2. SPK Fuzzy: Menghitung skor teladan dan perankingan mahasiswa
3. Profil Developer 
""")

# ------ Dataframe --------

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "data_sampel.csv")
    df = pd.read_csv(file_path)
    return df.sample(300, random_state=42)

df = load_data()
st.dataframe(df)



with st.form("my_form"):
    text = st.text_area(label="Input GPA", placeholder="Example: 4.0")
    submitted = st.form_submit_button("Submit")
    # if not :
    #     st.info("Please add your OpenAI API key to continue.")
    # elif submitted:
    #     generate_response(text)

st.markdown("---")
st.caption("Dibuat untuk memenuhi tugas akhir Praktikum SCPK")
