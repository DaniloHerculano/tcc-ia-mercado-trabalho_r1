import streamlit as st
import plotly.express as px
import json
import plotly.graph_objects as go

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
    # GRÁFICO
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
    
    import json
    import plotly.graph_objects as go
    
    st.subheader(
        "🗺️ Exposição IA por Estado"
    )
    
    # ======================================
    # AGRUPAR DADOS
    # ======================================
    
    mapa = (
        df.groupby("UF")
        .agg({
            "AIOE_SCORE": "mean",
            "Rendimento_Mensal": "mean"
        })
        .reset_index()
    )
    
    mapa["UF"] = (
        mapa["UF"]
        .astype(str)
        .str.upper()
    )
    
    # ======================================
    # GEOJSON LOCAL
    # ======================================
    
    with open(
    "data/brasil_estados.geojson",
    "r",
    encoding="utf-8"
    ) as f:
    
        geojson = json.load(f)
    
    st.write(
        geojson["features"][0]["properties"]
    )
    
    # ======================================
    # MAPA
    # ======================================
    
    fig_mapa = go.Figure(
    
        go.Choropleth(
    
            geojson=geojson,
    
            locations=mapa["UF"],
    
            z=mapa["AIOE_SCORE"],
    
            featureidkey="properties.sigla",
    
            colorscale="Reds",
    
            colorbar_title="AIOE",
    
            text=mapa["UF"],
    
            customdata=mapa[
                [
                    "Rendimento_Mensal"
                ]
            ],
    
            hovertemplate=
            "<b>UF:</b> %{text}<br>" +
            "<b>AIOE:</b> %{z:.2f}<br>" +
            "<b>Renda Média:</b> R$ %{customdata[0]:,.2f}<extra></extra>"
        )
    )
    
    # ======================================
    # LAYOUT
    # ======================================
    
    fig_mapa.update_geos(
    
        fitbounds="locations",
    
        visible=False
    )
    
    fig_mapa.update_layout(
    
        height=700,
    
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
