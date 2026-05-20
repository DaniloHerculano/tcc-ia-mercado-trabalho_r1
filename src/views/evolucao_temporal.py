import streamlit as st
import plotly.express as px


# ==========================================
# EVOLUÇÃO TEMPORAL
# ==========================================

def mostrar_evolucao_temporal(df):

    st.title(
        "📈 Evolução Temporal"
    )

    st.markdown("""
    Evolução temporal da base PNAD.
    """)

    st.divider()

    # ======================================
    # VALIDAR
    # ======================================

    if "Ano" not in df.columns:

        st.error(
            "Coluna Ano não encontrada."
        )

        return

    # ======================================
    # AGRUPAR
    # ======================================

    evolucao = (
        df.groupby("Ano")
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
        title="Evolução Temporal"
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