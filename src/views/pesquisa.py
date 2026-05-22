import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PESQUISA
# ==========================================

def mostrar_pesquisa(df):

    st.title(
        "🔎 Pesquisa Inteligente de Ocupações"
    )

    st.markdown("""
    Pesquise ocupações e visualize
    exposição à IA, renda e características.
    """)

    st.divider()

    # ======================================
    # VALIDAR
    # ======================================

    if "TITULO_LIMPO" not in df.columns:

        st.error(
            "Coluna TITULO_LIMPO não encontrada."
        )

        return

    # ======================================
    # LIMPEZA
    # ======================================

    pesquisa = df.copy()

    pesquisa["TITULO_LIMPO"] = (
        pesquisa["TITULO_LIMPO"]
        .astype(str)
    )

    pesquisa["AIOE_SCORE"] = pd.to_numeric(
        pesquisa["AIOE_SCORE"],
        errors="coerce"
    )

    pesquisa["Rendimento_Mensal"] = pd.to_numeric(
        pesquisa["Rendimento_Mensal"],
        errors="coerce"
    )

    # ======================================
    # INPUT
    # ======================================

    ocupacoes = sorted(
        pesquisa["TITULO_LIMPO"]
        .dropna()
        .unique()
    )

    ocupacao = st.selectbox(
        "Selecione uma ocupação",
        ocupacoes
    )

    st.divider()

    # ======================================
    # FILTRAR
    # ======================================

    dados = pesquisa[
        pesquisa["TITULO_LIMPO"] == ocupacao
    ]

    if len(dados) == 0:

        st.warning(
            "Nenhum dado encontrado."
        )

        return

    # ======================================
    # KPIs
    # ======================================

    media_ia = round(
        dados["AIOE_SCORE"].mean(),
        2
    )

    renda = round(
        dados["Rendimento_Mensal"].mean(),
        2
    )

    impacto = (
        dados["NIVEL_IMPACTO"]
        .mode()[0]
    )

    uf = (
        dados["UF"]
        .mode()[0]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🤖 Média IA",
        media_ia
    )

    col2.metric(
        "💰 Renda Média",
        f"R$ {renda:,.0f}"
    )

    col3.metric(
        "🚨 Impacto",
        impacto
    )

    col4.metric(
        "🌎 UF Frequente",
        uf
    )

    st.divider()

    # ======================================
    # DISTRIBUIÇÃO IA
    # ======================================

    fig = px.histogram(

        dados,

        x="AIOE_SCORE",

        nbins=20,

        title="Distribuição de Exposição IA"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # RENDA POR UF
    # ======================================

    renda_uf = (
        dados.groupby("UF")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(

        renda_uf,

        x="UF",

        y="Rendimento_Mensal",

        color="Rendimento_Mensal",

        title="Renda Média por Estado"
    )

    fig2.update_layout(
        height=500
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # EVOLUÇÃO TEMPORAL
    # ======================================

    if "Ano" in dados.columns:

        evolucao = (
            dados.groupby("Ano")
            ["AIOE_SCORE"]
            .mean()
            .reset_index()
        )

        fig3 = px.line(

            evolucao,

            x="Ano",

            y="AIOE_SCORE",

            markers=True,

            title="Evolução Temporal IA"
        )

        fig3.update_layout(
            height=500
        )

        st.plotly_chart(
            fig3,
            width='stretch'
        )

    st.divider()

    # ======================================
    # SIMILARES
    # ======================================

    st.subheader(
        "🧠 Ocupações Similares"
    )

    similares = pesquisa.copy()

    similares["DISTANCIA"] = (
        similares["AIOE_SCORE"] - media_ia
    ).abs()

    similares = similares[
        similares["TITULO_LIMPO"] != ocupacao
    ]

    similares = (
        similares.sort_values(
            by="DISTANCIA"
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_SCORE",
                "Rendimento_Mensal",
                "NIVEL_IMPACTO"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        similares,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    st.subheader(
        "🧠 Insights Automáticos"
    )

    if media_ia >= 0.75:

        st.warning(f"""
        A ocupação {ocupacao}
        possui ALTA exposição à IA.
        """)

    elif media_ia >= 0.45:

        st.info(f"""
        A ocupação {ocupacao}
        possui MÉDIA exposição à IA.
        """)

    else:

        st.success(f"""
        A ocupação {ocupacao}
        possui BAIXA exposição à IA.
        """)

    st.info(f"""
    💰 Renda média estimada:

    R$ {renda:,.0f}

    🌎 Estado mais frequente:

    {uf}
    """)
