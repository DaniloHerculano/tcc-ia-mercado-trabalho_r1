import streamlit as st
import plotly.express as px


# ==========================================
# ESCOLARIDADE
# ==========================================

def mostrar_escolaridade(df):

    st.title(
        "🎓 Escolaridade x IA"
    )

    st.markdown("""
    Relação entre formação profissional
    e exposição à Inteligência Artificial.
    """)

    st.divider()

    # ======================================
    # MÉDIA
    # ======================================

    escolaridade = (
        df.groupby("FORMAÇÃO E EXPERIÊNCIA")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    escolaridade = escolaridade.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    # ======================================
    # GRÁFICO
    # ======================================

    fig = px.bar(
        escolaridade,
        x="FORMAÇÃO E EXPERIÊNCIA",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Média de Exposição IA"
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
                "FORMAÇÃO E EXPERIÊNCIA",
                "NIVEL_IMPACTO"
            ]
        )
        .size()
        .reset_index(name="Quantidade")
    )

    fig2 = px.bar(
        impacto,
        x="FORMAÇÃO E EXPERIÊNCIA",
        y="Quantidade",
        color="NIVEL_IMPACTO",
        barmode="group",
        title="Distribuição de Impacto"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    maior = escolaridade.iloc[0]

    menor = escolaridade.iloc[-1]

    st.warning(f"""
    🎓 Formação mais exposta:

    {maior['FORMAÇÃO E EXPERIÊNCIA']}

    Média:
    {round(maior['AIOE_SCORE'], 2)}
    """)

    st.success(f"""
    📘 Formação menos exposta:

    {menor['FORMAÇÃO E EXPERIÊNCIA']}

    Média:
    {round(menor['AIOE_SCORE'], 2)}
    """)