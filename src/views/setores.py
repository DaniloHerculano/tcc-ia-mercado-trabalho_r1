import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json

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
        subset=[
            "COD_Grande_Grupo_TITULO",
            "AIOE_SCORE"
        ]
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
    # BAR CHART
    # ======================================

    fig = px.bar(
        grupo,
        x="COD_Grande_Grupo_TITULO",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Exposição IA por Grupo Ocupacional"
    )

    fig.update_layout(
        xaxis_title="Grupo Ocupacional",
        yaxis_title="Média AIOE"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # MAPA BRASIL
    # ======================================
    
    st.subheader(
        "🗺️ Exposição IA por Estado"
    )
    
    # ======================================
    # LAT/LONG ESTADOS
    # ======================================
    
    coords = {
        "AC": [-8.77, -70.55],
        "AL": [-9.71, -35.73],
        "AP": [1.41, -51.77],
        "AM": [-3.07, -61.66],
        "BA": [-12.96, -38.51],
        "CE": [-3.71, -38.54],
        "DF": [-15.83, -47.86],
        "ES": [-19.19, -40.34],
        "GO": [-16.64, -49.31],
        "MA": [-2.55, -44.30],
        "MT": [-12.64, -55.42],
        "MS": [-20.51, -54.54],
        "MG": [-18.10, -44.38],
        "PA": [-5.53, -52.29],
        "PB": [-7.06, -35.55],
        "PR": [-24.89, -51.55],
        "PE": [-8.28, -35.07],
        "PI": [-8.28, -43.68],
        "RJ": [-22.84, -43.15],
        "RN": [-5.22, -36.52],
        "RS": [-30.01, -51.22],
        "RO": [-11.22, -62.80],
        "RR": [1.89, -61.22],
        "SC": [-27.33, -49.44],
        "SP": [-23.55, -46.64],
        "SE": [-10.90, -37.07],
        "TO": [-10.25, -48.25]
    }
    
    # ======================================
    # AGRUPAR
    # ======================================
    
    mapa = (
        df.groupby("UF")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )
    
    mapa["UF"] = (
        mapa["UF"]
        .astype(str)
        .str.upper()
        .str.strip()
    )
    
    # ======================================
    # LAT/LONG
    # ======================================
    
    mapa["lat"] = mapa["UF"].apply(
        lambda x: coords[x][0]
        if x in coords else None
    )
    
    mapa["lon"] = mapa["UF"].apply(
        lambda x: coords[x][1]
        if x in coords else None
    )
    
    # ======================================
    # REMOVER INVÁLIDOS
    # ======================================
    
    mapa = mapa.dropna(
        subset=["lat", "lon"]
    )
    
    # ======================================
    # MAPA
    # ======================================
    
    fig_mapa = px.scatter_geo(
    
        mapa,
    
        lat="lat",
    
        lon="lon",
    
        size="AIOE_SCORE",
    
        color="AIOE_SCORE",
    
        hover_name="UF",
    
        color_continuous_scale="Reds",
    
        size_max=45,
    
        projection="natural earth",
    
        title="Mapa de Exposição IA por Estado"
    )
    
    fig_mapa.update_layout(
    
        height=700,
    
        geo=dict(
            scope="south america",
            center=dict(
                lat=-14,
                lon=-52
            ),
            projection_scale=4.5,
            showland=True
        ),
    
        margin=dict(
            l=0,
            r=0,
            t=40,
            b=0
        )
    )
    
    st.plotly_chart(
        fig_mapa,
        width='stretch'
    )
    
    st.divider()

    # ======================================
    # DISTRIBUIÇÃO IMPACTO
    # ======================================

    st.subheader(
        "📊 Distribuição de Impacto por Grupo"
    )

    impacto = (
        setores.groupby(
            [
                "COD_Grande_Grupo_TITULO",
                "NIVEL_IMPACTO"
            ]
        )
        .size()
        .reset_index(name="Quantidade")
    )

    fig2 = px.bar(
        impacto,
        x="COD_Grande_Grupo_TITULO",
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
        setores.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "COD_Grande_Grupo_TITULO",
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
    # TABELA FINAL
    # ======================================

    st.subheader(
        "📋 Média IA por Grupo"
    )

    st.dataframe(
        grupo,
        width='stretch'
    )
