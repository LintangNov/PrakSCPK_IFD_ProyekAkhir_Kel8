import streamlit as st

st.set_page_config(
    page_title="Profil Kelompok",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Profil Kelompok")
st.caption("Proyek Akhir Praktikum SCPK 2025/2026")

tab1, tab2, tab3 = st.tabs(["Anggota", "Tentang Sistem", "Referensi"])

with tab1:
    st.subheader("Anggota Kelompok")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Anggota A")
        st.markdown("""
        **Nama:** [Nama Anggota A]

        **NPM:** [NPM]

        **Kontribusi (60%):**
        - Implementasi fuzzy engine (scikit-fuzzy)
        - Definisi variabel dan fungsi keanggotaan
        - Penyusunan rule base Fuzzy Mamdani
        - Fungsi ranking dan simulasi individu
        - Testing dan debugging backend
        """)

    with col2:
        st.markdown("#### Anggota B")
        st.markdown("""
        **Nama:** [Nama Anggota B]

        **NPM:** [NPM]

        **Kontribusi (40%):**
        - Desain dan implementasi UI Streamlit
        - Halaman Data Explorer dan visualisasi
        - Integrasi fuzzy engine ke halaman SPK
        - Penulisan laporan akhir
        - Pengelolaan repository GitHub
        """)

with tab2:
    st.subheader("Tentang Sistem")
    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Ringkasan Sistem")
        st.markdown("""
        | Aspek | Keterangan |
        |---|---|
        | Nama Sistem | SPK Pemilihan Mahasiswa Teladan |
        | Metode | Fuzzy Mamdani (scikit-fuzzy) |
        | Platform | Python + Streamlit |
        | Input | 5 variabel antecedent |
        | Output | Skor Teladan (0-100) |
        | Dataset | 300 baris (sampled) |
        """)

    with col_b:
        st.markdown("#### Variabel Input")
        st.markdown("""
        | Variabel | Rentang | Himpunan |
        |---|---|---|
        | GPA | 1.9 - 4.0 | Rendah, Sedang, Tinggi |
        | Ekstrakurikuler | 0 - 12 jam/minggu | Pasif, Sedang, Aktif |
        | Olahraga | 0 - 10 jam/minggu | Kurang, Cukup, Sangat Aktif |
        | Screen Time | 1 - 12 jam/hari | Ideal, Berlebih |
        | Tingkat Stres | 1 - 9 | Rendah, Sedang, Tinggi |
        """)

    st.markdown("---")
    st.markdown("#### Output")
    st.markdown("""
    | Kategori | Rentang Skor | Keterangan |
    |---|---|---|
    | Kurang | 0 - 40 | Tidak direkomendasikan |
    | Layak | 40 - 70 | Cukup memenuhi syarat |
    | Sangat Layak | 70 - 100 | Sangat direkomendasikan |
    """)

with tab3:
    st.subheader("Referensi")
    st.markdown("---")
    st.markdown("""
    - scikit-fuzzy Documentation: https://pythonhosted.org/scikit-fuzzy/
    - Streamlit Documentation: https://docs.streamlit.io/
    - Pandas Documentation: https://pandas.pydata.org/docs/
    - Plotly Documentation: https://plotly.com/python/
    - Dataset: Global University Students Performance & Habits (Kaggle)

    ---
    **Mata Kuliah:** Sistem Pendukung Keputusan

    **Program Studi:** Informatika / Teknologi Informasi

    **Universitas:** UPN Veteran Yogyakarta

    **Tahun Akademik:** 2025 / 2026
    """)

st.markdown("---")
st.caption("Dibuat untuk memenuhi Proyek Akhir Praktikum SCPK 2025/2026 · UPN Veteran Yogyakarta")