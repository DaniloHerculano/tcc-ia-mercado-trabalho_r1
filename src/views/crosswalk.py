import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_crosswalk(df):
    
    st.title("🔗 Cobertura do Crosswalk Ocupacional")

    total = len(df)

    # ==============================
    # COBERTURA DO MERGE
    # ==============================
    merge_ok = df["CBO_EXTRAIDO"].notna().sum()

    pnad_ok = df["CBO_JOIN"].notna().sum()

    cbo_validos = df["CBO_JOIN"].notna().sum()

    aioe_ok = df["AIOE_SCORE"].notna().sum()

    dados = pd.DataFrame([
        {"Etapa": "PNAD válida", "Cobertura": pnad_ok / total * 100},
        {"Etapa": "CBO válido", "Cobertura": cbo_validos / total * 100},
        {"Etapa": "Merge CBO-PNAD", "Cobertura": merge_ok / total * 100},
        {"Etapa": "Score IA válido", "Cobertura": aioe_ok / total * 100},
    ])

    fig = px.bar(
        dados,
        x="Etapa",
        y="Cobertura",
        title="Cobertura por Etapa do Crosswalk Ocupacional",
        text_auto=".2f"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(dados)
