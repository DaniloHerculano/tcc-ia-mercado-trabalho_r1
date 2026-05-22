import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# DASHBOARD HOME
# ==========================================

def mostrar_dashboard(df):

    st.title(
        "📊 Dashboard Executivo"
    )

    st.markdown("""
    Panorama geral da exposição
    à Inteligência Artificial
    no mercado de trabalho brasileiro.
    """)

    st.divider()

    # ======================================
    # KPIs
    # ======================================

    total = len(df)

    media_aioe = round(
        df["AIOE_SCORE"].mean(),
        2
    )

    renda = round(
        df["Rendimento_Mensal"].mean(),
        2
    )

    alto = len(
        df[
            df["NIVEL_IMPACTO"] == "🔴 Alto"
        ]
    )

    perc_alto = round(
        (alto / total) * 100,
        2
    )

    uf = (
        df.groupby("UF")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    uf_ordenado = uf.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )
    
    uf_top = uf_ordenado.iloc[0]
    
    uf_bottom = uf_ordenado.iloc[-1]

    # ======================================
    # CARDS
    # ======================================

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "👥 Trabalhadores",
        f"{total:,}"
    )

    col2.metric(
        "🤖 Média IA",
        media_aioe
    )

    col3.metric(
        "💰 Renda Média",
        f"R$ {renda:,.0f}"
    )

    col4.metric(
        "🚨 Alto Impacto",
        f"{perc_alto}%"
    )

    col5.metric(
        "🌎 UF Mais Exposta",
        uf_top["UF"]
    )
    
    col6.metric(
        "📉 UF Menos Exposta",
        uf_bottom["UF"]
    )

    st.divider()

    # ======================================
    # LINHA 1
    # ======================================

    col1, col2 = st.columns(2)

    # ======================================
    # IMPACTO IA
    # ======================================

    with col1:

        impacto = (
            df.groupby("NIVEL_IMPACTO")
            .size()
            .reset_index(name="Quantidade")
        )

        fig = px.pie(

            impacto,

            names="NIVEL_IMPACTO",

            values="Quantidade",

            title="Distribuição de Impacto IA"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # ======================================
    # SEXO
    # ======================================

    with col2:

        sexo = (
            df.groupby("Sexo")
            .size()
            .reset_index(name="Quantidade")
        )

        fig2 = px.bar(

            sexo,

            x="Sexo",

            y="Quantidade",

            color="Sexo",

            title="Distribuição por Sexo"
        )

        st.plotly_chart(
            fig2,
            width='stretch'
        )

    st.divider()

    # ======================================
    # EVOLUÇÃO TEMPORAL
    # ======================================

    if "Ano" in df.columns:

        evolucao = (
            df.groupby("Ano")
            ["AIOE_SCORE"]
            .mean()
            .reset_index()
        )

        fig3 = px.line(

            evolucao,

            x="Ano",

            y="AIOE_SCORE",

            markers=True,

            title="Evolução Temporal da Exposição IA"
        )

        st.plotly_chart(
            fig3,
            width='stretch'
        )

    st.divider()

    # ======================================
    # TOP OCUPAÇÕES
    # ======================================

    st.subheader(
        "🚨 Top 10 Ocupações Mais Expostas"
    )

    top = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "UF",
                "AIOE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        top,
        width='stretch'
    )

    st.divider()

    # ======================================
    # NARRATIVA
    # ======================================

    st.subheader(
        "🧠 Resumo Executivo"
    )

    st.info(f"""
    Os dados analisados indicam que
    aproximadamente {perc_alto}% das ocupações
    apresentam alto potencial de impacto
    pela Inteligência Artificial.

    A média geral de exposição encontrada
    foi de {media_aioe}.

    O estado com maior exposição média
    foi {uf_top["UF"]}.
    
    Já o estado menos exposto
    foi {uf_bottom["UF"]}.
    """)
