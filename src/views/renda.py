import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# RENDA
# ==========================================

def mostrar_renda(df):

    st.title("💰 Renda x IA")

    if "Rendimento_Mensal" not in df.columns:

        st.error(
            "Coluna Rendimento_Mensal não encontrada."
        )

        return

    renda = df.copy()

    renda = renda.dropna(
        subset=["Rendimento_Mensal"]
    )

    if len(renda) == 0:

        st.warning("Sem dados de renda.")

        return

    renda["Faixa"] = pd.cut(
        renda["Rendimento_Mensal"],
        bins=[0, 1000, 2000, 5000, 10000, 20000, 999999],
        labels=[
            "Até 1k",
            "1k-2k",
            "2k-5k",
            "5k-10k",
            "10k-20k",
            "20k+"
        ]
    )

    distribuicao = (
        renda.groupby("Faixa")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.bar(
        distribuicao,
        x="Faixa",
        y="Quantidade",
        color="Quantidade",
        title="Distribuição Salarial"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.dataframe(
        distribuicao,
        width='stretch'
    )