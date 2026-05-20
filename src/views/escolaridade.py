import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_escolaridade(df):

    st.title("🎓 Escolaridade x IA")

    st.markdown("""
    Relação entre escolaridade
    e exposição à IA.
    """)

    # ======================================
    # VALIDAR
    # ======================================

    if "Anos_Estudo" not in df.columns:

        st.error("Coluna Anos_Estudo não encontrada.")

        return

    # ======================================
    # LIMPEZA
    # ======================================

    escolaridade = df.copy()

    escolaridade = escolaridade.dropna(
        subset=["Anos_Estudo"]
    )

    # ======================================
    # AGRUPAR
    # ======================================

    escolaridade = (
        escolaridade.groupby("Anos_Estudo")
        .size()
        .reset_index(name="Quantidade")
    )

    escolaridade = escolaridade.sort_values(
        by="Quantidade",
        ascending=False
    )

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        escolaridade,
        x="Anos_Estudo",
        y="Quantidade",
        color="Quantidade",
        title="Distribuição por Escolaridade"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    st.dataframe(
        escolaridade,
        width='stretch'
    )