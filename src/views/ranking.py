import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# RANKING
# ==========================================

def mostrar_ranking(df):

    st.title(
        "🏆 Ranking Inteligente"
    )

    st.markdown("""
    Ranking das ocupações brasileiras
    com maior e menor exposição à IA.
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

    ranking = df.copy()

    ranking["AIOE_SCORE"] = pd.to_numeric(
        ranking["AIOE_SCORE"],
        errors="coerce"
    )

    ranking["Rendimento_Mensal"] = pd.to_numeric(
        ranking["Rendimento_Mensal"],
        errors="coerce"
    )

    ranking = ranking.dropna(
        subset=[
            "TITULO_LIMPO",
            "AIOE_SCORE"
        ]
    )

    # ======================================
    # AGRUPAR
    # ======================================

    ranking = (
        ranking.groupby("TITULO_LIMPO")
        .agg({
            "AIOE_SCORE": "mean",
            "Rendimento_Mensal": "mean"
        })
        .reset_index()
    )

    # ======================================
    # FILTRO TOP N
    # ======================================

    top_n = st.slider(
        "Quantidade de ocupações",
        5,
        50,
        15
    )

    st.divider()

    # ======================================
    # TOP MAIS EXPOSTAS
    # ======================================

    st.subheader(
        "🚨 Ocupações Mais Expostas"
    )

    top = ranking.sort_values(
        by="AIOE_SCORE",
        ascending=False
    ).head(top_n)

    fig = px.bar(

        top,

        x="AIOE_SCORE",

        y="TITULO_LIMPO",

        orientation="h",

        color="AIOE_SCORE",

        title="Top Ocupações Mais Expostas"
    )

    fig.update_layout(
        height=700
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.dataframe(
        top,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP MENOS EXPOSTAS
    # ======================================

    st.subheader(
        "🛡️ Ocupações Menos Expostas"
    )

    baixo = ranking.sort_values(
        by="AIOE_SCORE",
        ascending=True
    ).head(top_n)

    fig2 = px.bar(

        baixo,

        x="AIOE_SCORE",

        y="TITULO_LIMPO",

        orientation="h",

        color="AIOE_SCORE",

        title="Top Ocupações Menos Expostas"
    )

    fig2.update_layout(
        height=700
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.dataframe(
        baixo,
        width='stretch'
    )

    st.divider()

    # ======================================
    # RENDA
    # ======================================

    st.subheader(
        "💰 IA x Renda"
    )

    renda = ranking.sort_values(
        by="Rendimento_Mensal",
        ascending=False
    ).head(top_n)

    fig3 = px.scatter(

        renda,

        x="Rendimento_Mensal",

        y="AIOE_SCORE",

        hover_name="TITULO_LIMPO",

        size="AIOE_SCORE",

        color="AIOE_SCORE",

        title="Renda x Exposição IA"
    )

    fig3.update_layout(
        height=700
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    st.subheader(
        "🧠 Insights Automáticos"
    )

    mais = top.iloc[0]

    menos = baixo.iloc[0]

    st.warning(f"""
    🚨 Ocupação mais exposta:

    {mais['TITULO_LIMPO']}

    Média AIOE:
    {round(mais['AIOE_SCORE'], 2)}
    """)

    st.success(f"""
    🛡️ Ocupação menos exposta:

    {menos['TITULO_LIMPO']}

    Média AIOE:
    {round(menos['AIOE_SCORE'], 2)}
    """)

    # ======================================
    # RESUMO
    # ======================================

    media = round(
        ranking["AIOE_SCORE"].mean(),
        2
    )

    st.info(f"""
    📊 Média geral de exposição IA:

    {media}

    O ranking mostra forte concentração
    de exposição em ocupações administrativas,
    analíticas e digitais.
    """)
