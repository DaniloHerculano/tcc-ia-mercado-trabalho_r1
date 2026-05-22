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
        title="Exposição IA por Grupo Ocupacional",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Grupo Ocupacional",
        yaxis_title="Média AIOE",
        height=600
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
    # GEOJSON
    # ======================================

    with open(
        "data/brasil_estados.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        brasil_geo = json.load(f)

    # ======================================
    # AGRUPAR
    # ======================================

    mapa = (
        df.groupby("UF")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    mapa = mapa.dropna()

    mapa["UF"] = (
        mapa["UF"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ======================================
    # MAPA DE CONVERSÃO
    # ======================================

    mapa_nome_estado = {

        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins"
    }

    # ======================================
    # CONVERTER NOMES
    # ======================================

    mapa["estado_nome"] = (
        mapa["UF"]
        .replace(mapa_nome_estado)
    )

    # ======================================
    # DEBUG
    # ======================================

    st.write("Estados encontrados:")
    st.write(mapa["estado_nome"].tolist())

    # ======================================
    # CHOROPLETH
    # ======================================

    fig_mapa = go.Figure(

        go.Choropleth(

            geojson=brasil_geo,

            locations=mapa["estado_nome"],

            z=mapa["AIOE_SCORE"],

            featureidkey="properties.name",

            colorscale="Reds",

            marker_line_width=1,

            marker_line_color="white",

            colorbar_title="AIOE",

            text=mapa["estado_nome"],

            hovertemplate=
            "<b>Estado:</b> %{text}<br>" +
            "<b>AIOE:</b> %{z:.2f}<extra></extra>"
        )
    )

    # ======================================
    # LAYOUT MAPA
    # ======================================

    fig_mapa.update_geos(

        fitbounds="locations",

        visible=False
    )

    fig_mapa.update_layout(

        title="Mapa de Calor IA por Estado",

        height=900,

        margin=dict(
            l=0,
            r=0,
            t=50,
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

    fig2.update_layout(
        height=650
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
