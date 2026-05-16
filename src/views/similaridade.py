import streamlit as st
import plotly.express as px


# ==========================================
# SIMILARIDADE
# ==========================================

def mostrar_similaridade(df):

    st.title(
        "🧠 Similaridade Semântica"
    )

    st.markdown("""
    Correspondência semântica entre
    ocupações brasileiras (CBO)
    e ocupações americanas
    do dataset AIOE/Felten.
    """)

    st.divider()

    # ======================================
    # HISTOGRAMA
    # ======================================

    fig = px.histogram(
        df,
        x="CONFIDENCE_SCORE",
        nbins=30,
        title="Distribuição da Similaridade"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP MATCHES
    # ======================================

    st.subheader(
        "🔥 Matches Mais Confiáveis"
    )

    top = (
        df.sort_values(
            by="CONFIDENCE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
                "CONFIDENCE_SCORE",
                "AIOE_SCORE"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        top,
        width='stretch'
    )

    st.divider()

    # ======================================
    # BAIXA CONFIANÇA
    # ======================================

    st.subheader(
        "⚠️ Matches com Baixa Similaridade"
    )

    baixo = (
        df.sort_values(
            by="CONFIDENCE_SCORE",
            ascending=True
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
                "CONFIDENCE_SCORE",
                "AIOE_SCORE"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        baixo,
        width='stretch'
    )

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    media = round(
        df["CONFIDENCE_SCORE"]
        .mean(),
        3
    )

    maior = round(
        df["CONFIDENCE_SCORE"]
        .max(),
        3
    )

    menor = round(
        df["CONFIDENCE_SCORE"]
        .min(),
        3
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Confiança Média",
        media
    )

    col2.metric(
        "Maior Similaridade",
        maior
    )

    col3.metric(
        "Menor Similaridade",
        menor
    )