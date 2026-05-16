import streamlit as st
import plotly.express as px


# ==========================================
# SETORES
# ==========================================

def mostrar_setores(df):

    st.title(
        "🏭 Setores x IA"
    )

    st.markdown("""
    Análise da exposição à Inteligência Artificial
    nos diferentes grupos ocupacionais.
    """)

    st.divider()

    # ======================================
    # MÉDIA POR GRUPO
    # ======================================

    grupo = (
        df.groupby("Grande Grupo")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    grupo = grupo.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    # ======================================
    # TOP SETORES
    # ======================================

    fig = px.bar(
        grupo,
        x="Grande Grupo",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Média de Exposição IA por Grande Grupo"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # DISTRIBUIÇÃO
    # ======================================

    impacto = (
        df.groupby(
            [
                "Grande Grupo",
                "NIVEL_IMPACTO"
            ]
        )
        .size()
        .reset_index(name="Quantidade")
    )

    fig2 = px.bar(
        impacto,
        x="Grande Grupo",
        y="Quantidade",
        color="NIVEL_IMPACTO",
        barmode="group",
        title="Distribuição de Impacto IA"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP OCUPAÇÕES
    # ======================================

    st.subheader(
        "🚨 Ocupações Mais Expostas"
    )

    top = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "Grande Grupo",
                "AIOE_SCORE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        top,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    maior = grupo.iloc[0]

    menor = grupo.iloc[-1]

    st.warning(f"""
    🏭 Grupo mais exposto:

    {maior['Grande Grupo']}

    Média AIOE:
    {round(maior['AIOE_SCORE'], 2)}
    """)

    st.success(f"""
    📉 Grupo menos exposto:

    {menor['Grande Grupo']}

    Média AIOE:
    {round(menor['AIOE_SCORE'], 2)}
    """)