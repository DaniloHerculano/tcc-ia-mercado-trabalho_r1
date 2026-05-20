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
        x="AIOE_SCORE",
        nbins=30,
        title="Distribuição AIOE"
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
        "🔥 Ocupações Mais Expostas"
    )

    top = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
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
    # BAIXA EXPOSIÇÃO
    # ======================================

    st.subheader(
        "⚠️ Ocupações Menos Expostas"
    )

    baixo = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=True
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
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
        df["AIOE_SCORE"]
        .mean(),
        3
    )

    maior = round(
        df["AIOE_SCORE"]
        .max(),
        3
    )

    menor = round(
        df["AIOE_SCORE"]
        .min(),
        3
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Média",
        media
    )

    col2.metric(
        "Maior Score",
        maior
    )

    col3.metric(
        "Menor Score",
        menor
    )