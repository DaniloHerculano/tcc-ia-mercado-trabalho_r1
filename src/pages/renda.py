import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# RENDA
# ==========================================

def mostrar_renda(df_pnad):

    st.title(
        "💰 Renda x IA"
    )

    st.markdown("""
    Análise da renda média da população
    trabalhadora brasileira utilizando
    dados da PNAD Contínua.
    """)

    st.divider()

    # ======================================
    # LIMPEZA
    # ======================================

    df = df_pnad.copy()

    df = df[
        df["Rendimento_Mensal"] > 0
    ]

    # ======================================
    # FAIXAS
    # ======================================

    df["FAIXA_RENDA"] = pd.cut(
        df["Rendimento_Mensal"],
        bins=[
            0,
            1000,
            2000,
            5000,
            10000,
            20000,
            100000
        ],
        labels=[
            "Até 1k",
            "1k-2k",
            "2k-5k",
            "5k-10k",
            "10k-20k",
            "20k+"
        ]
    )

    # ======================================
    # MÉDIA
    # ======================================

    renda = (
        df.groupby("FAIXA_RENDA")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        renda,
        x="FAIXA_RENDA",
        y="Rendimento_Mensal",
        color="Rendimento_Mensal",
        title="Renda Média por Faixa"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # SEXO
    # ======================================

    sexo = (
        df.groupby("Sexo")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig2 = px.pie(
        sexo,
        names="Sexo",
        values="Rendimento_Mensal",
        title="Distribuição Média Salarial"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # EVOLUÇÃO
    # ======================================

    evolucao = (
        df.groupby("Ano")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig3 = px.line(
        evolucao,
        x="Ano",
        y="Rendimento_Mensal",
        markers=True,
        title="Evolução da Renda Média"
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    media = round(
        df["Rendimento_Mensal"].mean(),
        2
    )

    maior = round(
        df["Rendimento_Mensal"].max(),
        2
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Renda Média",
        f"R$ {media}"
    )

    col2.metric(
        "Maior Renda",
        f"R$ {maior}"
    )