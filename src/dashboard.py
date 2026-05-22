import streamlit as st

from carregar_dados import (
    carregar_pnad,
    carregar_cbo,
    limpar_cbo,
    limpar_pnad,
    cruzar_bases
)

st.set_page_config(
    page_title="DEBUG",
    layout="wide"
)

st.title("DEBUG FINAL 2")

# ==========================================
# PNAD
# ==========================================

st.write("1 - Carregando PNAD")

df_pnad = carregar_pnad()

st.success("PNAD OK")

# ==========================================
# CBO
# ==========================================

st.write("2 - Carregando CBO")

df_cbo = carregar_cbo()

st.success("CBO OK")

# ==========================================
# LIMPEZA CBO
# ==========================================

st.write("3 - Limpando CBO")

df_cbo = limpar_cbo(df_cbo)

st.success("LIMPEZA CBO OK")

# ==========================================
# LIMPEZA PNAD
# ==========================================

st.write("4 - Limpando PNAD")

df_pnad = limpar_pnad(df_pnad)

st.success("LIMPEZA PNAD OK")

# ==========================================
# MERGE
# ==========================================

st.write("5 - Fazendo merge")

df_final = cruzar_bases(
    df_cbo,
    df_pnad
)

st.success("MERGE OK")

st.write(df_final.head())

st.write(df_final.columns.tolist())