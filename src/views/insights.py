import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# INSIGHTS
# ==========================================

def mostrar_insights(df):

    st.title(
        "🧠 Insights Inteligentes"
    )

    st.markdown("""
    Principais descobertas automáticas
    encontradas nos dados.
    """)

    st.divider()

    # ======================================
    # ESTADO MAIS EXPOSTO
    # ======================================

    uf = (
        df.groupby("UF")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    uf = uf.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    maior_uf = uf.iloc[0]

    menor_uf = uf.iloc[-1]

    # ======================================
    # GRUPO MAIS EXPOSTO
    # ======================================

    grupo = (
        df.groupby(
            "COD_Grande_Grupo_TITULO"
        )
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    grupo = grupo.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    maior_grupo = grupo.iloc[0]

    # ======================================
    # RENDA
    # ======================================

    renda = round(
        df["Rendimento_Mensal"].mean(),
        2
    )

    # ======================================
    # IDADE
    # ======================================

    idade = round(
        df["Idade"].mean(),
        1
    )

    # ======================================
    # IMPACTO
    # ======================================

    alto = len(
        df[
            df["NIVEL_IMPACTO"] == "🔴 Alto"
        ]
    )

    total = len(df)

    perc_alto = round(
        (alto / total) * 100,
        2
    )

    # ======================================
    # CARDS
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        st.warning(f"""
        🚨 Estado mais exposto:

        {maior_uf['UF']}

        Média AIOE:
        {round(maior_uf['AIOE_SCORE'], 2)}
        """)

    with col2:

        st.success(f"""
        📉 Estado menos exposto:

        {menor_uf['UF']}

        Média AIOE:
        {round(menor_uf['AIOE_SCORE'], 2)}
        """)

    st.divider()

    # ======================================
    # INSIGHTS TEXTUAIS
    # ======================================

    st.subheader(
        "📌 Principais Descobertas"
    )

    st.info(f"""
    🏭 O grupo ocupacional mais exposto
    à IA foi:

    {maior_grupo['COD_Grande_Grupo_TITULO']}

    com média AIOE de
    {round(maior_grupo['AIOE_SCORE'], 2)}.
    """)

    st.info(f"""
    💰 A renda média encontrada
    foi de aproximadamente:

    R$ {renda:,.2f}
    """)

    st.info(f"""
    🎂 A idade média dos trabalhadores
    analisados foi de:

    {idade} anos.
    """)

    st.info(f"""
    🤖 Aproximadamente
    {perc_alto}% dos trabalhadores
    estão em ocupações de alto
    impacto potencial por IA.
    """)

    st.divider()

    # ======================================
    # DISTRIBUIÇÃO IMPACTO
    # ======================================

    impacto = (
        df.groupby("NIVEL_IMPACTO")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.pie(

        impacto,

        names="NIVEL_IMPACTO",

        values="Quantidade",

        title="Distribuição Geral de Impacto IA"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP OCUPAÇÕES
    # ======================================

    st.subheader(
        "🚨 Top 15 Ocupações Mais Expostas"
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
        .head(15)
    )

    st.dataframe(
        top,
        width='stretch'
    )
