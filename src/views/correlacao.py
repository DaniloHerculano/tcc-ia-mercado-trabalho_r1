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
    # COPIAR
    # ======================================

    corr_df = df[colunas].copy()

    # ======================================
    # NUMÉRICOS
    # ======================================

    for col in colunas:

        corr_df[col] = pd.to_numeric(
            corr_df[col],
            errors="coerce"
        )

    # ======================================
    # REMOVER NAN
    # ======================================

    corr_df = corr_df.dropna()

    # DEBUG
    st.write("Total linhas válidas:")
    st.write(len(corr_df))

    st.write("Prévia:")
    st.write(corr_df.head())

    # ======================================
    # VALIDAR
    # ======================================

    if len(corr_df) == 0:

        st.error("""
        Nenhum dado válido encontrado
        para gerar correlação.
        """)

        return

    # ======================================
    # MATRIZ
    # ======================================

    matriz = corr_df.corr()

    st.write("Matriz:")
    st.write(matriz)

    # ======================================
    # HEATMAP
    # ======================================

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
        height=650
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

    # ======================================
    # INTERPRETAÇÃO
    # ======================================

    if corr_renda >= 0.3:

        st.success("""
        Ocupações com maior renda
        tendem a apresentar maior
        exposição à IA.
        """)

    elif corr_renda <= -0.3:

        st.warning("""
        Ocupações com menor renda
        apresentam maior exposição
        à IA.
        """)

    else:

        st.info("""
        A relação entre renda e IA
        foi fraca.
        """)
