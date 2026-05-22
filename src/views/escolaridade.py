import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# ESCOLARIDADE
# ==========================================

def mostrar_escolaridade(df):

    st.title("🎓 Escolaridade x IA")

    # ======================================
    # VALIDAR
    # ======================================

    if "Curso" not in df.columns:

        st.error("Coluna Curso não encontrada.")

        return

    # ======================================
    # LIMPEZA
    # ======================================

    escolaridade = df.copy()

    escolaridade = escolaridade.dropna(
        subset=["Curso"]
    )

    # ======================================
    # AGRUPAR
    # ======================================

    escolaridade = (
        escolaridade.groupby("Curso")
        .size()
        .reset_index(name="Quantidade")
    )

    escolaridade = escolaridade.sort_values(
        by="Quantidade",
        ascending=False
    ).head(20)

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        escolaridade,
        x="Curso",
        y="Quantidade",
        color="Quantidade",
        title="Distribuição por Curso"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.dataframe(
        escolaridade,
        width='stretch'
    )