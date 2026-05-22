import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# SIMULADOR IA
# ==========================================

def mostrar_simulador(df):

    st.title(
        "🤖 Simulador de Exposição à IA"
    )

    st.markdown("""
    Simule o potencial de exposição
    de perfis profissionais
    à Inteligência Artificial.
    """)

    st.divider()

    # ======================================
    # VALIDAR
    # ======================================

    colunas_necessarias = [

        "Rendimento_Mensal",
        "Idade",
        "Sexo",
        "UF",
        "AIOE_SCORE"
    ]

    for col in colunas_necessarias:

        if col not in df.columns:

            st.error(
                f"Coluna {col} não encontrada."
            )

            return

    # ======================================
    # FILTROS
    # ======================================

    col1, col2 = st.columns(2)

    with col1:

        idade = st.slider(
            "🎂 Idade",
            18,
            80,
            30
        )

        renda = st.slider(
            "💰 Renda Mensal",
            500,
            30000,
            5000,
            step=500
        )

    with col2:

        sexo = st.selectbox(
            "👤 Sexo",
            sorted(
                df["Sexo"]
                .dropna()
                .unique()
            )
        )

        uf = st.selectbox(
            "🌎 UF",
            sorted(
                df["UF"]
                .dropna()
                .unique()
            )
        )

    st.divider()

    # ======================================
    # BASE FILTRADA
    # ======================================

    base = df.copy()

    base = base.dropna(
        subset=[
            "AIOE_SCORE",
            "Rendimento_Mensal",
            "Idade"
        ]
    )

    base["Rendimento_Mensal"] = pd.to_numeric(
        base["Rendimento_Mensal"],
        errors="coerce"
    )

    base["Idade"] = pd.to_numeric(
        base["Idade"],
        errors="coerce"
    )

    # ======================================
    # SCORE SIMPLES
    # ======================================

    score_base = (
        base["AIOE_SCORE"]
        .mean()
    )

    ajuste_renda = (
        renda / 30000
    ) * 0.25

    ajuste_idade = (
        idade / 80
    ) * 0.15

    score = (
        score_base
        + ajuste_renda
        + ajuste_idade
    )

    score = min(
        max(score, 0),
        1
    )

    # ======================================
    # CLASSIFICAÇÃO
    # ======================================

    if score >= 0.75:

        nivel = "🔴 Alto"

    elif score >= 0.45:

        nivel = "🟡 Médio"

    else:

        nivel = "🟢 Baixo"

    # ======================================
    # KPIS
    # ======================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🤖 Score IA",
        round(score, 2)
    )

    col2.metric(
        "📊 Impacto",
        nivel
    )

    col3.metric(
        "💰 Renda",
        f"R$ {renda:,.0f}"
    )

    st.divider()

    # ======================================
    # VELOCÍMETRO
    # ======================================

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            number={
                "suffix": ""
            },

            title={
                "text": "Exposição à IA"
            },

            gauge={

                "axis": {
                    "range": [0, 1]
                },

                "bar": {
                    "thickness": 0.3
                },

                "steps": [

                    {
                        "range": [0, 0.45],
                        "color": "green"
                    },

                    {
                        "range": [0.45, 0.75],
                        "color": "gold"
                    },

                    {
                        "range": [0.75, 1],
                        "color": "red"
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # OCUPAÇÕES SIMILARES
    # ======================================

    st.subheader(
        "🧠 Ocupações com Perfil Similar"
    )

    similares = base.copy()

    similares = similares[
        (similares["Sexo"] == sexo)
        &
        (similares["UF"] == uf)
    ]

    similares["DISTANCIA"] = (

        abs(
            similares["Idade"] - idade
        )

        +

        abs(
            similares["Rendimento_Mensal"] - renda
        ) / 1000
    )

    similares = similares.sort_values(
        by="DISTANCIA"
    )

    colunas = [

        "TITULO_LIMPO",
        "UF",
        "Sexo",
        "Idade",
        "Rendimento_Mensal",
        "AIOE_SCORE",
        "NIVEL_IMPACTO"
    ]

    colunas_existentes = [

        c for c in colunas

        if c in similares.columns
    ]

    st.dataframe(

        similares[
            colunas_existentes
        ].head(10),

        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHT
    # ======================================

    st.info(f"""
    📌 O perfil simulado apresentou
    score médio de exposição IA de
    {round(score, 2)}.

    Classificação estimada:
    {nivel}

    A análise considera características
    semelhantes encontradas na base PNAD.
    """)
