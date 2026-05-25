import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Data Explorer", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "..", "data", "data_sampel.csv")
    df = pd.read_csv(file_path)
    return df.sample(300, random_state=42)

df = load_data()

with st.sidebar:
    st.title("Filters")

    selected_majors = st.multiselect(
        "Major",
        options=sorted(df["major"].unique().tolist()),
        default=sorted(df["major"].unique().tolist()),
    )
    selected_countries = st.multiselect(
        "Country",
        options=sorted(df["country"].unique().tolist()),
        default=sorted(df["country"].unique().tolist()),
    )
    gpa_range = st.slider(
        "GPA Range",
        min_value=float(df["GPA"].min()),
        max_value=float(df["GPA"].max()),
        value=(float(df["GPA"].min()), float(df["GPA"].max())),
        step=0.01,
    )

df_filtered = df[
    (df["major"].isin(selected_majors)) &
    (df["country"].isin(selected_countries)) &
    (df["GPA"] >= gpa_range[0]) &
    (df["GPA"] <= gpa_range[1])
]

st.title("Data Explorer")
st.caption(f"Menampilkan {len(df_filtered)} dari {len(df)} data mahasiswa setelah filter diterapkan.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Mahasiswa", len(df_filtered))
col2.metric("Rata-rata GPA", f"{df_filtered['GPA'].mean():.2f}")
col3.metric("Rata-rata Stress", f"{df_filtered['mental_stress_level'].mean():.2f}")
col4.metric("Rata-rata Ekskul", f"{df_filtered['extracurricular_hours_per_week'].mean():.1f} jam/minggu")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Overview", "Distribusi", "Eksplorasi per Jurusan"])

with tab1:
    st.subheader("GPA vs Tingkat Stres")
    st.caption(
        "Grafik ini menantang asumsi umum bahwa mahasiswa berprestasi (GPA tinggi) selalu ideal. "
        "Perhatikan mahasiswa dengan GPA tinggi namun tingkat stres yang juga tinggi."
    )

    fig_scatter = px.scatter(
        df_filtered,
        x="GPA",
        y="mental_stress_level",
        color="major",
        hover_data=["student_id", "country", "extracurricular_hours_per_week", "screen_time_hours"],
        labels={
            "GPA": "GPA",
            "mental_stress_level": "Tingkat Stres",
            "major": "Jurusan",
        },
        template="plotly_white",
        opacity=0.75,
    )
    fig_scatter.update_traces(marker=dict(size=7))
    fig_scatter.update_layout(
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Distribusi GPA")
        st.caption("Sebaran nilai GPA dari seluruh mahasiswa yang difilter.")
        fig_hist = px.histogram(
            df_filtered,
            x="GPA",
            nbins=25,
            color_discrete_sequence=["#4C78A8"],
            labels={"GPA": "GPA", "count": "Jumlah"},
            template="plotly_white",
        )
        fig_hist.update_layout(height=350, bargap=0.05, showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.subheader("Distribusi Tingkat Stres")
        st.caption("Sebaran tingkat stres mahasiswa. Stres tinggi menunjukkan kondisi yang tidak ideal meski GPA bagus.")
        fig_stress = px.histogram(
            df_filtered,
            x="mental_stress_level",
            nbins=20,
            color_discrete_sequence=["#E45756"],
            labels={"mental_stress_level": "Tingkat Stres", "count": "Jumlah"},
            template="plotly_white",
        )
        fig_stress.update_layout(height=350, bargap=0.05, showlegend=False)
        st.plotly_chart(fig_stress, use_container_width=True)

with tab2:
    st.subheader("Distribusi Variabel")
    st.caption("Pilih variabel untuk melihat sebarannya. Distribusi yang tidak homogen menjadi alasan penggunaan Fuzzy.")

    var_options = {
        "GPA": "GPA",
        "Ekstrakurikuler (jam/minggu)": "extracurricular_hours_per_week",
        "Olahraga (jam/minggu)": "exercise_hours_per_week",
        "Screen Time (jam/hari)": "screen_time_hours",
        "Tingkat Stres": "mental_stress_level",
    }

    selected_var_label = st.selectbox("Pilih variabel:", list(var_options.keys()))
    selected_var = var_options[selected_var_label]

    fig_dist = px.histogram(
        df_filtered,
        x=selected_var,
        nbins=25,
        color_discrete_sequence=["#54A24B"],
        labels={selected_var: selected_var_label, "count": "Jumlah Mahasiswa"},
        template="plotly_white",
    )
    fig_dist.update_layout(height=400, bargap=0.05, showlegend=False)
    st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")
    st.subheader("GPA vs Variabel Lain")
    st.caption("Lihat hubungan antara GPA dan variabel pilihan. Apakah GPA tinggi selalu sejalan dengan kondisi ideal?")

    compare_options = {k: v for k, v in var_options.items() if v != "GPA"}
    selected_compare_label = st.selectbox("Bandingkan GPA dengan:", list(compare_options.keys()))
    selected_compare = compare_options[selected_compare_label]

    fig_compare = px.scatter(
        df_filtered,
        x="GPA",
        y=selected_compare,
        color="major",
        trendline="ols",
        hover_data=["student_id", "country"],
        labels={"GPA": "GPA", selected_compare: selected_compare_label, "major": "Jurusan"},
        template="plotly_white",
        opacity=0.7,
    )
    fig_compare.update_layout(
        height=430,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_compare, use_container_width=True)

with tab3:
    st.subheader("Rata-rata Variabel per Jurusan")
    st.caption(
        "Perbandingan rata-rata setiap variabel antar jurusan. "
        "Membantu melihat apakah ada jurusan yang secara rata-rata memiliki kondisi tidak ideal."
    )

    var_bar_options = {
        "GPA": "GPA",
        "Ekstrakurikuler (jam/minggu)": "extracurricular_hours_per_week",
        "Olahraga (jam/minggu)": "exercise_hours_per_week",
        "Screen Time (jam/hari)": "screen_time_hours",
        "Tingkat Stres": "mental_stress_level",
    }

    selected_bar_label = st.selectbox("Pilih variabel:", list(var_bar_options.keys()), key="bar_var")
    selected_bar = var_bar_options[selected_bar_label]

    avg_per_major = (
        df_filtered.groupby("major")[selected_bar]
        .mean()
        .reset_index()
        .sort_values(selected_bar, ascending=True)
    )

    fig_bar = px.bar(
        avg_per_major,
        x=selected_bar,
        y="major",
        orientation="h",
        color=selected_bar,
        color_continuous_scale="Blues",
        labels={selected_bar: f"Rata-rata {selected_bar_label}", "major": "Jurusan"},
        template="plotly_white",
    )
    fig_bar.update_layout(height=420, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.subheader("Raw Data")
    st.caption("Dataset mentah setelah filter diterapkan.")
    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True, height=350)