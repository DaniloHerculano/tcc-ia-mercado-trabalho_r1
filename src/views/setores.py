import streamlit as st
import plotly.express as px

# ==========================================
# SETORES
# ==========================================

def mostrar_setores(df):

    st.title(
        "🏭 Grandes Grupos Ocupacionais"
    )

    st.markdown("""
    Análise da exposição à IA
    por grupos ocupacionais brasileiros.
    """)

    st.divider()

    # ======================================
    # VALIDAR
    # ======================================

    if "COD_Grande_Grupo_TITULO" not in df.columns:

        st.error(
            "Coluna COD_Grande_Grupo_TITULO não encontrada."
        )

        return

    # ======================================
    # LIMPEZA
    # ======================================

    setores = df.dropna(
        subset=["COD_Grande_Grupo_TITULO"]
    )

    # ======================================
    # MÉDIA POR GRUPO
    # ======================================

    grupo = (
        setores.groupby(
            "COD_Grande_Grupo_TITULO"
        )
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
        x="COD_Grande_Grupo_TITULO",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Exposição IA por Grupo Ocupacional"
    )

    st.plotly_chart(
        fig,
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
        🚨 Grupo mais exposto:

        {maior['COD_Grande_Grupo_TITULO']}

        Média:
        {round(maior['AIOE_SCORE'], 2)}
        """)

        st.success(f"""
        📉 Grupo menos exposto:

        {menor['COD_Grande_Grupo_TITULO']}

        Média:
        {round(menor['AIOE_SCORE'], 2)}
        """)

    st.divider()

    # ======================================
    # TABELA
    # ======================================

    st.dataframe(
        grupo,
        width='stretch'
    )
