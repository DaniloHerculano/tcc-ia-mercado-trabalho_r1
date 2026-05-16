import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_escolaridade(df, df_pnad):

    st.title("🎓 Escolaridade x IA")

    st.markdown("""
    Relação entre escolaridade
    e exposição à IA.
    """)

    # ======================================
    # VALIDAR
    # ======================================

    if "Anos_Estudo" not in df_pnad.columns:

        st.error("Coluna Anos_Estudo não encontrada.")

        return

    # ======================================
    # AGRUPAR
    # ======================================

    escolaridade = (
        df_pnad.groupby("Anos_Estudo")
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