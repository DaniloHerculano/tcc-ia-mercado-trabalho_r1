import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# RENDA
# ==========================================

def mostrar_renda(df):

    st.title("💰 Renda x IA")

    st.markdown("""
    Distribuição salarial
    da base PNAD.
    """)

    # ======================================
    # VALIDAR
    # ======================================

    if "Rendimento_Mensal" not in df.columns:

        st.error("Coluna Rendimento_Mensal não encontrada.")

        return

    # ======================================
    # LIMPEZA
    # ======================================

    renda = df.copy()

    renda = renda.dropna(
        subset=["Rendimento_Mensal"]
    )

    # ======================================
    # FAIXAS
    # ======================================

    renda["Faixa"] = pd.cut(
        renda["Rendimento_Mensal"],
        bins=[0, 1000, 2000, 5000, 10000, 20000],
        labels=[
            "Até 1k",
            "1k-2k",
            "2k-5k",
            "5k-10k",
            "10k-20k"
        ]
    )

    distribuicao = (
        renda.groupby("Faixa")
        .size()
        .reset_index(name="Quantidade")
    )

    # ======================================
    # GRÁFICO
    # ======================================

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

    st.divider()

    st.dataframe(
        distribuicao,
        width='stretch'
    )