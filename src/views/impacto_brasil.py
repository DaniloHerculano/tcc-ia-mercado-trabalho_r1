import streamlit as st
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
    utilizando dados da PNAD Contínua.
    """)

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    total = len(df)

    media_idade = round(
        df["Idade"].mean(),
        1
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
        "Trabalhadores",
        f"{total:,}"
    )

    col2.metric(
        "Idade Média",
        media_idade
    )

    col3.metric(
        "Renda Média",
        f"R$ {media_renda}"
    )

    col4.metric(
        "Estados",
        total_ufs
    )

    st.divider()

    # ======================================
    # UF
    # ======================================

    uf = (
        df["UF"]
        .value_counts()
        .reset_index()
    )

    uf.columns = [
        "UF",
        "Quantidade"
    ]

    fig = px.bar(
        uf,
        x="UF",
        y="Quantidade",
        color="Quantidade",
        title="Distribuição por UF"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # SEXO
    # ======================================

    sexo = (
        df["Sexo"]
        .value_counts()
        .reset_index()
    )

    sexo.columns = [
        "Sexo",
        "Quantidade"
    ]

    fig2 = px.pie(
        sexo,
        names="Sexo",
        values="Quantidade",
        title="Distribuição por Sexo"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )