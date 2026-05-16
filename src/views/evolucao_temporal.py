import streamlit as st
import plotly.express as px


# ==========================================
# EVOLUÇÃO TEMPORAL
# ==========================================

def mostrar_evolucao_temporal(
    df_pnad
):

    st.title(
        "📅 Evolução Temporal"
    )

    st.markdown("""
    Evolução da força de trabalho
    brasileira ao longo do tempo.
    """)

    st.divider()

    # ======================================
    # EVOLUÇÃO BASE
    # ======================================

    evolucao = (
        df_pnad.groupby("Ano")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.line(
        evolucao,
        x="Ano",
        y="Quantidade",
        markers=True,
        title="Evolução da Base PNAD"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # RENDA
    # ======================================

    renda = (
        df_pnad.groupby("Ano")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig2 = px.line(
        renda,
        x="Ano",
        y="Rendimento_Mensal",
        markers=True,
        title="Renda Média ao Longo do Tempo"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # IDADE
    # ======================================

    idade = (
        df_pnad.groupby("Ano")
        ["Idade"]
        .mean()
        .reset_index()
    )

    fig3 = px.line(
        idade,
        x="Ano",
        y="Idade",
        markers=True,
        title="Idade Média ao Longo do Tempo"
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )