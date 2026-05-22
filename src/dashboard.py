import streamlit as st
import traceback

st.title("DEBUG TOTAL")

try:

    from carregar_dados import criar_base_final

    st.success("Import OK")

    df = criar_base_final()

    st.success("Base criada!")

    st.write(df.head())

except Exception as e:

    st.error("ERRO DETALHADO:")

    st.code(traceback.format_exc())