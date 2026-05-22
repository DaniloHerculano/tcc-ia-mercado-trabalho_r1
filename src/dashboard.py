import streamlit as st
import pandas as pd

from carregar_dados import (
    carregar_pnad,
    carregar_cbo
)

st.set_page_config(
    page_title="DEBUG",
    layout="wide"
)

st.title("DEBUG FINAL")

# ==========================================
# TESTE PNAD
# ==========================================

try:

    st.write("TESTE PARQUET")

    df_pnad = carregar_pnad()

    st.success("PARQUET OK")

    st.write(df_pnad.head())

except Exception as e:

    st.error(f"ERRO PARQUET: {e}")

# ==========================================
# TESTE CBO
# ==========================================

try:

    st.write("TESTE CBO")

    df_cbo = carregar_cbo()

    st.success("CBO OK")

    st.write(df_cbo.head())

except Exception as e:

    st.error(f"ERRO CBO: {e}")