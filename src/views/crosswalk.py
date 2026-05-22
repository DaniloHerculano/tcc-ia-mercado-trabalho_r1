import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_crosswalk(df):

    st.title("🔗 Cobertura por etapa do crosswalk ocupacional")

    # ============================
    # DADOS (IGUAL AO GRÁFICO)
    # ============================

    dados = pd.DataFrame([
        {"Etapa": "CBO → ISCO-88", "Cobertura": 100.0},
        {"Etapa": "ISCO-88 → ISCO-08", "Cobertura": 100.0},
        {"Etapa": "ISCO-08 → SOC", "Cobertura": 100.0},
        {"Etapa": "SOC → Felten/AIOE", "Cobertura": 78.2},
        {"Etapa": "ISCO-08 → Gmyrek Exposure", "Cobertura": 76.8},
        {"Etapa": "ISCO-08 → Gmyrek Mean", "Cobertura": 76.8},
        {"Etapa": "ISCO-08 → Gmyrek SD", "Cobertura": 76.8},
        {"Etapa": "CBO → COD", "Cobertura": 98.7},
    ])

    # ============================
    # ORDEM (IMPORTANTE)
    # ============================

    dados = dados.iloc[::-1]  # deixa igual ao gráfico da imagem

    # ============================
    # GRÁFICO
    # ============================

    fig = px.bar(
        dados,
        x="Cobertura",
        y="Etapa",
        orientation="h",
        text="Cobertura",
        title="Cobertura por etapa do crosswalk ocupacional"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        xaxis_range=[0, 100],
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # ============================
    # LEGENDA / RODAPÉ (TCC STYLE)
    # ============================

    st.caption(
        "Imagem: gráfico da porcentagem de códigos ocupacionais transformados por etapa. Fonte: Autores do TCC."
    )
