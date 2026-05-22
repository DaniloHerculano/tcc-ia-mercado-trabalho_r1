import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# ESCOLARIDADE
# ==========================================

def mostrar_escolaridade(df):

    st.title("🎓 Escolaridade x IA")

    st.markdown("""
    Relação entre formação profissional
    e exposição à Inteligência Artificial.
    """)

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
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    escolaridade = escolaridade.sort_values(
        by="AIOE_SCORE",
        ascending=False
    ).head(20)

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        escolaridade,
        x="Curso",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Cursos com Maior Exposição à IA"
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

    # ======================================
    # INSIGHT
    # ======================================

    if len(escolaridade) > 0:

        maior = escolaridade.iloc[0]

        st.warning(f"""
        📌 Curso mais exposto:

        {maior['Curso']}

        Média AIOE:
        {round(maior['AIOE_SCORE'], 2)}
        """)
