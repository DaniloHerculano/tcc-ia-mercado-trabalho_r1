import streamlit as st

from carregar_dados import criar_base_final

st.set_page_config(
    page_title="DEBUG",
    layout="wide"
)

st.title("DEBUG DASHBOARD")

try:

    df = criar_base_final()

    st.success("Base carregada!")

    st.write(df.head())

except Exception as e:

    st.error("Erro ao carregar base")
    st.exception(e)