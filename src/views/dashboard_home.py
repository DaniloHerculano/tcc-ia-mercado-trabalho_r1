import streamlit as st
import plotly.express as px


# ==========================================
# DASHBOARD HOME
# ==========================================

def mostrar_dashboard(df):

    st.title(
        "🤖 IA e Mercado de Trabalho"
    )

    st.markdown("""
    Plataforma de análise do impacto da
    Inteligência Artificial nas ocupações
    brasileiras utilizando NLP, embeddings
    semânticos e similaridade de cosseno.
    """)

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    total = len(df)

    media_aioe = round(
        df["AIOE_SCORE"].mean(),
        2
    )

    maior_score = round(
        df["AIOE_SCORE"].max(),
        2
    )

    media_conf = round(
        df["CONFIDENCE_SCORE"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total de Ocupações",
        total
    )

    col2.metric(
        "Média AIOE",
        media_aioe
    )

    col3.metric(
        "Maior Score",
        maior_score
    )

    col4.metric(
        "Confiança Média",
        media_conf
    )

    st.divider()

    # ======================================
    # IMPACTO
    # ======================================

    impacto = (
        df["NIVEL_IMPACTO"]
        .value_counts()
        .reset_index()
    )

    impacto.columns = [
        "Impacto",
        "Quantidade"
    ]

    fig = px.bar(
        impacto,
        x="Impacto",
        y="Quantidade",
        color="Impacto",
        title="Distribuição de Impacto"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP 10
    # ======================================

    st.subheader(
        "🔥 Ocupações Mais Expostas"
    )

    top10 = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "CBO_EXTRAIDO",
                "TITULO_LIMPO",
                "AIOE_SCORE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        top10,
        width='stretch'
    )