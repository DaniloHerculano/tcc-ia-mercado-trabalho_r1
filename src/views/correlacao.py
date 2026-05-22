import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# CORRELAÇÃO
# ==========================================

def mostrar_correlacao(df):

    st.title(
        "🔥 Correlação entre Variáveis"
    )

    st.markdown("""
    Relação entre renda, idade,
    exposição à IA e outras variáveis.
    """)

    st.divider()

    # ======================================
    # COLUNAS
    # ======================================

    colunas = [

        "Idade",
        "Rendimento_Mensal",
        "AIOE_SCORE"
    ]

    # ======================================
    # VALIDAR
    # ======================================

    faltando = [
        c for c in colunas
        if c not in df.columns
    ]

    if len(faltando) > 0:

        st.error(f"""
        Colunas faltando:

        {faltando}
        """)

        return

    # ======================================
    # DATAFRAME
    # ======================================

    corr_df = df[colunas].copy()

    for col in colunas:

        corr_df[col] = pd.to_numeric(
            corr_df[col],
            errors="coerce"
        )

    corr_df = corr_df.dropna()

    # ======================================
    # VALIDAR
    # ======================================

    if len(corr_df) == 0:

        st.error("""
        Nenhum dado válido encontrado.
        """)

        return

    # ======================================
    # MATRIZ
    # ======================================

    matriz = corr_df.corr()

    # ======================================
    # HEATMAP
    # ======================================

    st.subheader(
        "🧠 Heatmap de Correlação"
    )

    fig = px.imshow(

        matriz,

        text_auto=".2f",

        color_continuous_scale="RdBu_r",

        zmin=-1,
        zmax=1,

        aspect="auto",

        title="Mapa de Correlação"
    )

    fig.update_layout(
        height=700
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # SCATTER IA X RENDA
    # ======================================

    st.subheader(
        "💰 IA x Renda"
    )

    amostra = corr_df.sample(
        min(len(corr_df), 3000)
    )

    fig2 = px.scatter(

        amostra,
    
        x="Rendimento_Mensal",
    
        y="AIOE_SCORE",
    
        title="Correlação entre IA e Renda"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # IA X IDADE
    # ======================================

    st.subheader(
        "🎂 IA x Idade"
    )

    fig3 = px.scatter(

        amostra,
    
        x="Idade",
    
        y="AIOE_SCORE",
    
        title="Correlação entre IA e Idade"
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

    corr_renda = round(
        matriz.loc[
            "AIOE_SCORE",
            "Rendimento_Mensal"
        ],
        2
    )

    corr_idade = round(
        matriz.loc[
            "AIOE_SCORE",
            "Idade"
        ],
        2
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "💰 IA x Renda",
            corr_renda
        )

    with col2:

        st.metric(
            "🎂 IA x Idade",
            corr_idade
        )

    st.divider()

    # ======================================
    # INTERPRETAÇÃO
    # ======================================

    st.subheader(
        "📌 Interpretação"
    )

    if corr_renda >= 0.30:

        st.success("""
        Ocupações com maior renda
        tendem a possuir maior
        exposição à IA.
        """)

    elif corr_renda <= -0.30:

        st.warning("""
        Ocupações com menor renda
        apresentam maior exposição
        à IA.
        """)

    else:

        st.info("""
        A relação entre renda e IA
        foi considerada fraca.
        """)

    # ======================================
    # TABELA
    # ======================================

    st.subheader(
        "📋 Dados de Correlação"
    )

    st.dataframe(
        matriz,
        width='stretch'
    )
