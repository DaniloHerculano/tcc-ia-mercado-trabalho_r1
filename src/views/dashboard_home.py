import streamlit as st
import plotly.express as px

# ==========================================
# DASHBOARD HOME
# ==========================================

def mostrar_dashboard(df):

    st.title(
        "🤖 IA e Mercado de Trabalho Brasileiro"
    )

    st.markdown("""
    Plataforma analítica sobre o impacto da
    Inteligência Artificial no mercado de trabalho
    brasileiro utilizando dados da PNAD Contínua,
    CBO e métricas AIOE/Felten.
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

    media_renda = round(
        df["Rendimento_Mensal"].mean(),
        2
    )

    media_idade = round(
        df["Idade"].mean(),
        1
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Trabalhadores",
        f"{total:,}"
    )

    col2.metric(
        "🤖 Média AIOE",
        media_aioe
    )

    col3.metric(
        "💰 Renda Média",
        f"R$ {media_renda:,.0f}"
    )

    col4.metric(
        "🎂 Idade Média",
        media_idade
    )

    st.divider()

    # ======================================
    # DISTRIBUIÇÃO IMPACTO
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

    fig = px.pie(
        impacto,
        names="Impacto",
        values="Quantidade",
        title="Distribuição Geral de Impacto IA"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP UFs
    # ======================================

    st.subheader(
        "🌎 Média de Exposição IA por UF"
    )

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

    fig2 = px.bar(
        uf,
        x="UF",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Exposição Média IA por Estado"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # EVOLUÇÃO TEMPORAL
    # ======================================

    st.subheader(
        "📈 Evolução Temporal"
    )

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
        title="Média AIOE ao Longo do Tempo"
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
        "🔥 Ocupações Mais Expostas"
    )

    top10 = (
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
        top10,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS AUTOMÁTICOS
    # ======================================

    maior_uf = uf.iloc[0]

    menor_uf = uf.iloc[-1]

    st.success(f"""
    📌 Estado mais exposto à IA:

    {maior_uf['UF']}

    Média AIOE:
    {round(maior_uf['AIOE_SCORE'], 2)}
    """)

    st.info(f"""
    📉 Estado menos exposto à IA:

    {menor_uf['UF']}

    Média AIOE:
    {round(menor_uf['AIOE_SCORE'], 2)}
    """)
