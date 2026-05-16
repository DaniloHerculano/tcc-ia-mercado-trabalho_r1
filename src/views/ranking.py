import streamlit as st
import plotly.express as px


# ==========================================
# RANKING
# ==========================================

def mostrar_ranking(df):

    st.title(
        "🏆 Ranking Geral"
    )

    st.markdown("""
    Ranking das ocupações brasileiras
    com maior exposição à IA.
    """)

    st.divider()

    # ======================================
    # FILTROS
    # ======================================

    top_n = st.slider(
        "Quantidade",
        10,
        100,
        20
    )

    impacto = st.selectbox(
        "Impacto",
        [
            "Todos",
            "🔴 Alto",
            "🟡 Médio",
            "🟢 Baixo"
        ]
    )

    # ======================================
    # FILTRAR
    # ======================================

    ranking = df.copy()

    if impacto != "Todos":

        ranking = ranking[
            ranking["NIVEL_IMPACTO"]
            == impacto
        ]

    ranking = ranking.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    ranking = ranking.head(top_n)

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        ranking,
        x="AIOE_SCORE",
        y="TITULO_LIMPO",
        color="NIVEL_IMPACTO",
        orientation="h",
        title="Ranking de Exposição IA"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TABELA
    # ======================================

    st.dataframe(
        ranking[
            [
                "CBO_EXTRAIDO",
                "TITULO_LIMPO",
                "Grande Grupo",
                "AIOE_SCORE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ],
        width='stretch'
    )