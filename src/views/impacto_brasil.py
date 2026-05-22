import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# IMPACTO BRASIL
# ==========================================

def mostrar_impacto_brasil(df):

    st.title(
        "🇧🇷 Impacto da IA no Brasil"
    )

    st.markdown("""
    Análise da força de trabalho brasileira
    utilizando dados da PNAD Contínua
    e métricas de exposição à IA.
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

    total_ufs = (
        df["UF"]
        .nunique()
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
        "🌎 Estados",
        total_ufs
    )

    st.divider()

    # ======================================
    # MÉDIA IA POR UF
    # ======================================

    uf = (
        df.groupby("UF")
        .agg({
            "AIOE_SCORE": "mean",
            "Rendimento_Mensal": "mean"
        })
        .reset_index()
    )

    uf = uf.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    # ======================================
    # BAR CHART UF
    # ======================================

    fig = px.bar(
        uf,
        x="UF",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        hover_data=[
            "Rendimento_Mensal"
        ],
        title="Média de Exposição IA por Estado"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # MÉDIA IA POR SEXO
    # ======================================

    st.subheader(
        "📊 Média IA por Sexo"
    )

    sexo_df = df.copy()

    sexo_df = sexo_df.dropna(
        subset=["Sexo", "AIOE_SCORE"]
    )

    sexo_df["Sexo"] = (
        sexo_df["Sexo"]
        .astype(str)
        .str.strip()
    )

    sexo_df["AIOE_SCORE"] = pd.to_numeric(
        sexo_df["AIOE_SCORE"],
        errors="coerce"
    )

    sexo = (
        sexo_df.groupby("Sexo")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    sexo = sexo.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    fig2 = px.bar(
        sexo,
        x="Sexo",
        y="AIOE_SCORE",
        color="Sexo",
        text_auto=".2f",
        title="Média IA por Sexo"
    )

    fig2.update_layout(
        yaxis_title="Média AIOE",
        xaxis_title="Sexo"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # IDADE
    # ======================================

    st.subheader(
        "🎂 Idade x Exposição IA"
    )

    amostra = df.sample(
        min(len(df), 3000)
    )

    fig3 = px.scatter(
        amostra,
        x="Idade",
        y="AIOE_SCORE",
        color="NIVEL_IMPACTO",
        title="Idade vs Exposição IA"
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP ESTADOS
    # ======================================

    st.subheader(
        "🏆 Estados Mais Expostos"
    )

    st.dataframe(
        uf.head(10),
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    if len(uf) > 0:

        maior = uf.iloc[0]

        menor = uf.iloc[-1]

        st.warning(f"""
        🚨 Estado mais exposto à IA:

        {maior['UF']}

        Média AIOE:
        {round(maior['AIOE_SCORE'], 2)}
        """)

        st.success(f"""
        📉 Estado menos exposto à IA:

        {menor['UF']}

        Média AIOE:
        {round(menor['AIOE_SCORE'], 2)}
        """)
