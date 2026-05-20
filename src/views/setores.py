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
    nos estados brasileiros.
    """)

    st.divider()

    # ======================================
    # MÉDIA POR UF
    # ======================================

    grupo = (
        df.groupby("UF")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    grupo = grupo.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        grupo,
        x="UF",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Média de Exposição IA por UF"
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
                "UF",
                "NIVEL_IMPACTO"
            ]
        )
        .size()
        .reset_index(name="Quantidade")
    )

    fig2 = px.bar(
        impacto,
        x="UF",
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
                "UF",
                "AIOE_SCORE",
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

    if len(grupo) > 0:

        maior = grupo.iloc[0]

        menor = grupo.iloc[-1]

        st.warning(f"""
        🏭 UF mais exposta:

        {maior['UF']}

        Média AIOE:
        {round(maior['AIOE_SCORE'], 2)}
        """)

        st.success(f"""
        📉 UF menos exposta:

        {menor['UF']}

        Média AIOE:
        {round(menor['AIOE_SCORE'], 2)}
        """)