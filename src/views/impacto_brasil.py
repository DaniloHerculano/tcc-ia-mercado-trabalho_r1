import streamlit as st
import plotly.express as px


# ==========================================
# IMPACTO BRASIL
# ==========================================

def mostrar_impacto_brasil(
    df,
    df_pnad
):

    st.title(
        "🇧🇷 Impacto da IA no Brasil"
    )

    st.markdown("""
    Análise da força de trabalho brasileira
    utilizando dados da PNAD Contínua
    e scores de exposição à IA.
    """)

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    total = len(df_pnad)

    media_idade = round(
        df_pnad["Idade"].mean(),
        1
    )

    media_renda = round(
        df_pnad["Rendimento_Mensal"].mean(),
        2
    )

    total_ufs = (
        df_pnad["UF"]
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

    st.subheader(
        "📍 Trabalhadores por Estado"
    )

    uf = (
        df_pnad["UF"]
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

    st.subheader(
        "👥 Distribuição por Sexo"
    )

    sexo = (
        df_pnad["Sexo"]
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

    st.divider()

    # ======================================
    # IDADE
    # ======================================

    st.subheader(
        "📈 Distribuição de Idade"
    )

    fig3 = px.histogram(
        df_pnad,
        x="Idade",
        nbins=30,
        title="Distribuição Etária"
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )