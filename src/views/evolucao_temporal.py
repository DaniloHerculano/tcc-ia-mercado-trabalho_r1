import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_evolucao_temporal(df, df_pnad):

    st.title("📈 Evolução Temporal")

    st.markdown("""
    Evolução temporal da força de trabalho
    brasileira ao longo dos anos.
    """)

    # ======================================
    # VALIDAR
    # ======================================

    if "Ano" not in df_pnad.columns:

        st.error("Coluna Ano não encontrada.")

        return

    # ======================================
    # AGRUPAMENTO
    # ======================================

    evolucao = (
        df_pnad.groupby("Ano")
        .size()
        .reset_index(name="Quantidade")
    )

    evolucao = evolucao.sort_values(
        by="Ano"
    )

    # ======================================
    # GRÁFICO
    # ======================================

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

    st.dataframe(
        evolucao,
        width='stretch'
    )