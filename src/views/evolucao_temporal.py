import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# EVOLUÇÃO TEMPORAL
# ==========================================

def mostrar_evolucao_temporal(df):

    st.title(
        "📈 Evolução Temporal"
    )

    st.markdown("""
    Evolução da exposição à IA
    ao longo do tempo no Brasil.
    """)

    st.divider()

    # ======================================
    # VALIDAR
    # ======================================

    if "Ano" not in df.columns:

        st.error(
            "Coluna Ano não encontrada."
        )

        return

    # ======================================
    # LIMPEZA
    # ======================================

    temporal = df.copy()

    temporal["Ano"] = pd.to_numeric(
        temporal["Ano"],
        errors="coerce"
    )

    temporal["AIOE_SCORE"] = pd.to_numeric(
        temporal["AIOE_SCORE"],
        errors="coerce"
    )

    temporal["Rendimento_Mensal"] = pd.to_numeric(
        temporal["Rendimento_Mensal"],
        errors="coerce"
    )

    temporal = temporal.dropna(
        subset=[
            "Ano",
            "AIOE_SCORE"
        ]
    )

    # ======================================
    # MÉDIA IA POR ANO
    # ======================================

    evolucao = (
        temporal.groupby("Ano")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    # ======================================
    # LINHA IA
    # ======================================

    fig = px.line(

        evolucao,

        x="Ano",

        y="AIOE_SCORE",

        markers=True,

        title="Evolução da Exposição à IA"
    )

    fig.update_layout(
        yaxis_title="Média AIOE",
        xaxis_title="Ano",
        height=600
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # RENDA TEMPORAL
    # ======================================

    renda = (
        temporal.groupby("Ano")
        ["Rendimento_Mensal"]
        .mean()
        .reset_index()
    )

    fig2 = px.line(

        renda,

        x="Ano",

        y="Rendimento_Mensal",

        markers=True,

        title="Evolução da Renda Média"
    )

    fig2.update_layout(
        yaxis_title="Renda Média",
        xaxis_title="Ano",
        height=600
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # EVOLUÇÃO POR SEXO
    # ======================================

    if "Sexo" in temporal.columns:

        sexo = (
            temporal.groupby(
                [
                    "Ano",
                    "Sexo"
                ]
            )
            ["AIOE_SCORE"]
            .mean()
            .reset_index()
        )

        fig3 = px.line(

            sexo,

            x="Ano",

            y="AIOE_SCORE",

            color="Sexo",

            markers=True,

            title="Evolução IA por Sexo"
        )

        fig3.update_layout(
            height=600
        )

        st.plotly_chart(
            fig3,
            width='stretch'
        )

        st.divider()

    # ======================================
    # EVOLUÇÃO POR UF
    # ======================================

    if "UF" in temporal.columns:

        uf = (
            temporal.groupby(
                [
                    "Ano",
                    "UF"
                ]
            )
            ["AIOE_SCORE"]
            .mean()
            .reset_index()
        )

        top_ufs = (
            temporal.groupby("UF")
            ["AIOE_SCORE"]
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .index
        )

        uf = uf[
            uf["UF"].isin(top_ufs)
        ]

        fig4 = px.line(

            uf,

            x="Ano",

            y="AIOE_SCORE",

            color="UF",

            markers=True,

            title="Top 5 UFs Mais Expostas"
        )

        fig4.update_layout(
            height=650
        )

        st.plotly_chart(
            fig4,
            width='stretch'
        )

    st.divider()

    # ======================================
    # COMPARAÇÃO ANOS
    # ======================================

    st.subheader(
        "⚖️ Comparação Temporal"
    )

    anos = sorted(
        temporal["Ano"]
        .dropna()
        .unique()
    )

    if len(anos) >= 2:

        primeiro = anos[0]
        ultimo = anos[-1]

        ia_inicio = round(
            evolucao.iloc[0]["AIOE_SCORE"],
            2
        )

        ia_final = round(
            evolucao.iloc[-1]["AIOE_SCORE"],
            2
        )

        crescimento = round(
            (
                (ia_final - ia_inicio)
                / ia_inicio
            ) * 100,
            2
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📅 Primeiro Ano",
            primeiro
        )

        col2.metric(
            "📅 Último Ano",
            ultimo
        )

        col3.metric(
            "📈 Crescimento IA",
            f"{crescimento}%"
        )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    st.subheader(
        "🧠 Insights Automáticos"
    )

    if crescimento > 0:

        st.success(f"""
        A exposição média à IA aumentou
        aproximadamente {crescimento}%
        no período analisado.
        """)

    else:

        st.warning("""
        Não foi identificado crescimento
        relevante na exposição à IA.
        """)

    # ======================================
    # TABELA
    # ======================================

    st.subheader(
        "📋 Evolução IA"
    )

    st.dataframe(
        evolucao,
        width='stretch'
    )
