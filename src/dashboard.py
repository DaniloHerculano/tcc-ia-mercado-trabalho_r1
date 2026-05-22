import streamlit as st

st.set_page_config(
    page_title="TESTE",
    layout="wide"
)

st.title("TESTE INICIAL")

try:

    import carregar_dados

    st.success("carregar_dados importado!")

except Exception as e:

    st.error("ERRO AO IMPORTAR carregar_dados")
    st.exception(e)