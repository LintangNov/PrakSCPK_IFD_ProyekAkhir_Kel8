import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
import os
import sys

matplotlib.use("Agg")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

from fuzzy_engine import rank, single_inference
import skfuzzy as fuzz
from skfuzzy import control as ctrl

st.set_page_config(
    page_title="SPK Fuzzy", layout="wide", initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    file_path = os.path.join(BASE_DIR, "..", "data", "data_sampel.csv")
    df = pd.read_csv(file_path)
    return df.sample(300, random_state=42)


@st.cache_data
def run_ranking(df_json):
    df = pd.read_json(df_json)
    return rank(df)


def get_kategori(skor):
    if skor >= 70:
        return "Sangat Layak"
    elif skor >= 40:
        return "Layak"
    else:
        return "Kurang"


def warna_kategori(kategori):
    if kategori == "Sangat Layak":
        return "background-color: #d4edda; color: #155724;"
    elif kategori == "Layak":
        return "background-color: #fff3cd; color: #856404;"
    else:
        return "background-color: #f8d7da; color: #721c24;"


df = load_data()

st.title("SPK Fuzzy Scoring & Ranking")
st.caption("Sistem Pendukung Keputusan Mahasiswa Teladan berbasis Fuzzy Mamdani.")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    ["Fungsi Keanggotaan", "Simulator Individu", "Ranking & Analisis"]
)

# ============================================================
# TAB 1: FUNGSI KEANGGOTAAN
# ============================================================
with tab1:
    st.subheader("Visualisasi Fungsi Keanggotaan")
    st.caption(
        "Kurva berikut menunjukkan bagaimana sistem Fuzzy Mamdani mendefinisikan batas linguistik "
        "setiap variabel input. Tidak ada batas tegas, melainkan derajat keanggotaan (0 sampai 1) "
        "yang merepresentasikan ketidakpastian penilaian manusia."
    )

    mf_configs = [
        {
            "label": "GPA",
            "universe": np.arange(1.9, 4.01, 0.01),
            "sets": {
                "Rendah": ("trimf", [1.9, 1.9, 2.8]),
                "Sedang": ("trimf", [2.5, 3.2, 3.7]),
                "Tinggi": ("trimf", [3.5, 4.0, 4.0]),
            },
            "colors": {
                "Rendah": ("#E45756", "rgba(228,87,86,0.12)"),
                "Sedang": ("#F58518", "rgba(245,133,24,0.12)"),
                "Tinggi": ("#54A24B", "rgba(84,162,75,0.12)"),
            },
        },
        {
            "label": "Ekstrakurikuler (jam/minggu)",
            "universe": np.arange(0, 12.5, 0.1),
            "sets": {
                "Pasif": ("trimf", [0, 0, 4]),
                "Sedang": ("trimf", [2, 6, 9]),
                "Aktif": ("trimf", [7, 12, 12]),
            },
            "colors": {
                "Pasif": ("#E45756", "rgba(228,87,86,0.12)"),
                "Sedang": ("#F58518", "rgba(245,133,24,0.12)"),
                "Aktif": ("#54A24B", "rgba(84,162,75,0.12)"),
            },
        },
        {
            "label": "Olahraga (jam/minggu)",
            "universe": np.arange(0, 10.5, 0.1),
            "sets": {
                "Kurang": ("trimf", [0, 0, 4]),
                "Cukup": ("trimf", [2, 5, 7]),
                "Sangat Aktif": ("trimf", [6, 10, 10]),
            },
            "colors": {
                "Kurang": ("#E45756", "rgba(228,87,86,0.12)"),
                "Cukup": ("#F58518", "rgba(245,133,24,0.12)"),
                "Sangat Aktif": ("#54A24B", "rgba(84,162,75,0.12)"),
            },
        },
        {
            "label": "Screen Time (jam/hari)",
            "universe": np.arange(1, 12.5, 0.1),
            "sets": {
                "Ideal": ("trapmf", [1, 1, 3, 5]),
                "Berlebih": ("trapmf", [4, 6, 12, 12]),
            },
            "colors": {
                "Ideal": ("#54A24B", "rgba(84,162,75,0.12)"),
                "Berlebih": ("#E45756", "rgba(228,87,86,0.12)"),
            },
        },
        {
            "label": "Tingkat Stres",
            "universe": np.arange(1, 9.5, 0.1),
            "sets": {
                "Rendah": ("trimf", [1, 1, 4]),
                "Sedang": ("trimf", [2.5, 5, 7]),
                "Tinggi": ("trimf", [6, 9, 9]),
            },
            "colors": {
                "Rendah": ("#54A24B", "rgba(84,162,75,0.12)"),
                "Sedang": ("#F58518", "rgba(245,133,24,0.12)"),
                "Tinggi": ("#E45756", "rgba(228,87,86,0.12)"),
            },
        },
        {
            "label": "Skor Teladan (Output)",
            "universe": np.arange(0, 101, 1),
            "sets": {
                "Kurang": ("trimf", [0, 0, 40]),
                "Layak": ("trimf", [30, 50, 70]),
                "Sangat Layak": ("trimf", [60, 100, 100]),
            },
            "colors": {
                "Kurang": ("#E45756", "rgba(228,87,86,0.12)"),
                "Layak": ("#F58518", "rgba(245,133,24,0.12)"),
                "Sangat Layak": ("#54A24B", "rgba(84,162,75,0.12)"),
            },
        },
    ]

    col_left, col_right = st.columns(2)

    for i, cfg in enumerate(mf_configs):
        fig = go.Figure()

        for set_name, (func_type, params) in cfg["sets"].items():
            universe = cfg["universe"]
            if func_type == "trimf":
                y = fuzz.trimf(universe, params)
            else:
                y = fuzz.trapmf(universe, params)

            line_color, fill_color = cfg["colors"][set_name]

            fig.add_trace(go.Scatter(
                x=universe,
                y=y,
                mode="lines",
                name=set_name,
                line=dict(color=line_color, width=2.5),
                fill="tozeroy",
                fillcolor=fill_color,
            )
        )

        fig.update_layout(
            title=dict(text=cfg["label"], font=dict(size=14)),
            xaxis_title=cfg["label"],
            yaxis_title="Derajat Keanggotaan (μ)",
            yaxis=dict(range=[0, 1.1]),
            template="plotly_white",
            height=280,
            margin=dict(l=40, r=20, t=50, b=40),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        if i % 2 == 0:
            col_left.plotly_chart(fig, use_container_width=True)
        else:
            col_right.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: SIMULATOR INDIVIDU
# ============================================================
with tab2:
    st.subheader("Simulator Individu")
    st.caption(
        "Masukkan nilai variabel untuk mensimulasikan skor kelayakan satu mahasiswa."
    )

    col_input, col_output = st.columns([1, 1])

    with col_input:
        gpa_input = st.slider("GPA", min_value=1.9, max_value=4.0, value=3.5, step=0.01)
        ekskul_input = st.slider(
            "Ekstrakurikuler (jam/minggu)",
            min_value=0.0,
            max_value=12.0,
            value=5.0,
            step=0.1,
        )
        olahraga_input = st.slider(
            "Olahraga (jam/minggu)", min_value=0.0, max_value=10.0, value=3.0, step=0.1
        )
        screen_input = st.slider(
            "Screen Time (jam/hari)", min_value=1.0, max_value=12.0, value=5.0, step=0.1
        )
        stress_input = st.slider(
            "Tingkat Stres", min_value=1.0, max_value=9.0, value=4.0, step=0.1
        )
        hitung = st.button("Hitung Skor", type="primary", use_container_width=True)

    with col_output:
        if hitung:
            try:
                skor = single_inference(
                    gpa_input, ekskul_input, olahraga_input, screen_input, stress_input
                )
                kategori = get_kategori(skor)

                st.metric("Skor Teladan", f"{skor:.1f} / 100")

                if kategori == "Sangat Layak":
                    st.success(f"Kategori: {kategori}")
                elif kategori == "Layak":
                    st.warning(f"Kategori: {kategori}")
                else:
                    st.error(f"Kategori: {kategori}")

                st.markdown("**Defuzzifikasi Output (Centroid)**")
                st.caption(
                    "Area berwarna menunjukkan himpunan output yang aktif setelah rule-rule dieksekusi. "
                    "Garis vertikal adalah titik crisp result dari metode centroid."
                )

                universe_out = np.arange(0, 101, 1)
                kurang = fuzz.trimf(universe_out, [0, 0, 40])
                layak = fuzz.trimf(universe_out, [30, 50, 70])
                sangat_layak = fuzz.trimf(universe_out, [60, 100, 100])

                aktivasi_kurang = min(
                    1.0, max(0.0, fuzz.interp_membership(universe_out, kurang, skor))
                )
                aktivasi_layak = min(
                    1.0, max(0.0, fuzz.interp_membership(universe_out, layak, skor))
                )
                aktivasi_sangat_layak = min(
                    1.0,
                    max(0.0, fuzz.interp_membership(universe_out, sangat_layak, skor)),
                )

                fig_defuzz = go.Figure()

                fig_defuzz.add_trace(
                    go.Scatter(
                        x=universe_out,
                        y=np.minimum(aktivasi_kurang, kurang),
                        fill="tozeroy",
                        name="Kurang (aktif)",
                        line=dict(color="#E45756", width=1.5),
                        fillcolor="rgba(228, 87, 86, 0.3)",
                    )
                )
                fig_defuzz.add_trace(
                    go.Scatter(
                        x=universe_out,
                        y=np.minimum(aktivasi_layak, layak),
                        fill="tozeroy",
                        name="Layak (aktif)",
                        line=dict(color="#F58518", width=1.5),
                        fillcolor="rgba(245, 133, 24, 0.3)",
                    )
                )
                fig_defuzz.add_trace(
                    go.Scatter(
                        x=universe_out,
                        y=np.minimum(aktivasi_sangat_layak, sangat_layak),
                        fill="tozeroy",
                        name="Sangat Layak (aktif)",
                        line=dict(color="#54A24B", width=1.5),
                        fillcolor="rgba(84, 162, 75, 0.3)",
                    )
                )

                fig_defuzz.add_vline(
                    x=skor,
                    line_dash="dash",
                    line_color="#4C78A8",
                    line_width=2,
                    annotation_text=f"Crisp: {skor:.1f}",
                    annotation_position="top right",
                )

                fig_defuzz.update_layout(
                    xaxis_title="Skor Teladan",
                    yaxis_title="Derajat Keanggotaan (μ)",
                    yaxis=dict(range=[0, 1.1]),
                    template="plotly_white",
                    height=320,
                    margin=dict(l=40, r=20, t=30, b=40),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                )
                st.plotly_chart(fig_defuzz, use_container_width=True)

            except Exception as e:
                st.error(f"Error saat kalkulasi: {e}")
        else:
            st.info("Atur nilai variabel di sebelah kiri, lalu tekan Hitung Skor.")

# ============================================================
# TAB 3: RANKING & ANALISIS
# ============================================================
with tab3:
    st.subheader("Perangkingan Mahasiswa")
    st.caption(
        "Klik tombol untuk menjalankan proses scoring fuzzy pada seluruh dataset."
    )

    if st.button("Jalankan Perangkingan", type="primary"):
        with st.spinner("Menghitung skor fuzzy untuk seluruh mahasiswa..."):
            result = run_ranking(df.to_json())
            result["kategori"] = result["skor_teladan"].apply(get_kategori)
            st.session_state["ranking_result"] = result

    if "ranking_result" in st.session_state:
        result = st.session_state["ranking_result"]
        result["peringkat"] = range(1, len(result) + 1)

        st.markdown("---")

        c1, c2, c3 = st.columns(3)
        c1.metric("Sangat Layak", len(result[result["kategori"] == "Sangat Layak"]))
        c2.metric("Layak", len(result[result["kategori"] == "Layak"]))
        c3.metric("Kurang", len(result[result["kategori"] == "Kurang"]))

        st.markdown("---")

        st.subheader("Tabel Hasil Perangkingan")
        display_cols = [
            "peringkat",
            "student_id",
            "major",
            "country",
            "GPA",
            "extracurricular_hours_per_week",
            "exercise_hours_per_week",
            "screen_time_hours",
            "mental_stress_level",
            "skor_teladan",
            "kategori",
        ]
        st.dataframe(
            result[display_cols].reset_index(drop=True),
            use_container_width=True,
            height=400,
        )

        st.markdown("---")

        st.subheader("Top 15 Mahasiswa")
        st.caption("Mahasiswa dengan skor teladan tertinggi.")

        top15 = result.head(15).copy()
        fig_top = px.bar(
            top15,
            x="skor_teladan",
            y="student_id",
            orientation="h",
            color="kategori",
            color_discrete_map={
                "Sangat Layak": "#54A24B",
                "Layak": "#F58518",
                "Kurang": "#E45756",
            },
            hover_data=["major", "country", "GPA", "mental_stress_level"],
            labels={
                "skor_teladan": "Skor Teladan",
                "student_id": "Student ID",
                "kategori": "Kategori",
            },
            template="plotly_white",
        )
        fig_top.update_layout(
            height=480,
            yaxis=dict(autorange="reversed"),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(fig_top, use_container_width=True)

        st.markdown("---")

        st.subheader("GPA vs Skor Teladan")
        st.caption(
            "Grafik ini membuktikan bahwa GPA tinggi tidak otomatis menghasilkan skor teladan tinggi. "
            "Faktor stres, screen time, olahraga, dan ekskul turut menentukan."
        )

        fig_gpa_skor = px.scatter(
            result,
            x="GPA",
            y="skor_teladan",
            color="kategori",
            color_discrete_map={
                "Sangat Layak": "#54A24B",
                "Layak": "#F58518",
                "Kurang": "#E45756",
            },
            hover_data=[
                "student_id",
                "major",
                "mental_stress_level",
                "screen_time_hours",
            ],
            labels={
                "GPA": "GPA",
                "skor_teladan": "Skor Teladan",
                "kategori": "Kategori",
            },
            template="plotly_white",
            opacity=0.75,
        )
        fig_gpa_skor.update_traces(marker=dict(size=7))
        fig_gpa_skor.update_layout(
            height=450,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )
        st.plotly_chart(fig_gpa_skor, use_container_width=True)
