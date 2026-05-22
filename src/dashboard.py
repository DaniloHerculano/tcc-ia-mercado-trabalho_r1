import streamlit as st

from carregar_dados import (
    criar_base_final
)

st.set_page_config(
    page_title="DEBUG",
    layout="wide"
)

st.title("DEBUG")

@st.cache_data
def carregar():

    return criar_base_final()

try:

    df = carregar()

    st.success("DATAFRAME CARREGADO")

    st.write(df.head())

    st.write(df.columns.tolist())

except Exception as e:

    st.error(str(e))