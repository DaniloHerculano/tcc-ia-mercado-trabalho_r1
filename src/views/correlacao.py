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
        "AIOE_SCORE",
        "Exposure",
        "Mean",
        "SD"
    ]

    existentes = [
        c for c in colunas
        if c in df.columns
    ]

    # ======================================
    # DATAFRAME
    # ======================================

    corr_df = df[existentes].copy()

    for col in existentes:

        corr_df[col] = pd.to_numeric(
            corr_df[col],
            errors="coerce"
        )

    corr_df = corr_df.dropna()

    # ======================================
    # MATRIZ
    # ======================================

    matriz = corr_df.corr(
        numeric_only=True
    )

    # ======================================
    # HEATMAP
    # ======================================

    fig = px.imshow(
        matriz,

        text_auto=".2f",

        color_continuous_scale="RdBu_r",

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
    # INSIGHTS
    # ======================================

    st.subheader(
        "🧠 Insights Automáticos"
    )

    try:

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

        st.info(f"""
        💰 Correlação IA x Renda:
        {corr_renda}
        """)

        st.info(f"""
        🎂 Correlação IA x Idade:
        {corr_idade}
        """)

        if corr_renda > 0:

            st.success("""
            Ocupações com maior renda
            tendem a apresentar maior
            exposição à IA.
            """)

        else:

            st.warning("""
            Não foi encontrada correlação
            positiva entre renda e IA.
            """)

    except:

        st.warning(
            "Não foi possível gerar insights."
        )
