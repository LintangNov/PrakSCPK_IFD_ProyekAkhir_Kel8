import streamlit as st
import pandas as pd
import os

# ------ Dataframe --------

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "data_sampel.csv")
    df = pd.read_csv(file_path)
    return df.sample(300, random_state=42)

df = load_data()
st.dataframe(df)


with st.sidebar:
    st.title(":material/filter_alt: Filters")
    selected_period = st.selectbox(
        "Reporting Period",
        ["1 Month", "3 Months", "6 Months", "12 Months", "24 Months", "All Time"],
        index=3,
        key="period",
        bind="query-params",
    )
    selected_markets = st.multiselect(
        "Market",
        # options=sorted(df["market"].unique().to_list()),
        default=[],
        key="market",
        bind="query-params",
    )
    selected_categories = st.multiselect(
        "Category",
        # options=sorted(df["category"].unique().to_list()),
        default=[],
        key="category",
        bind="query-params",
    )
