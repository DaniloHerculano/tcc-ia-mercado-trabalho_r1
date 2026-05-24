import streamlit as st
import plotly.express as px
import pandas as pd
import json


# ==========================================
# GRANDES GRUPOS OCUPACIONAIS
# ==========================================

def mostrar_setores(df):

    st.title("🏭 Mapa de Exposição a IA")

    st.markdown("""
    Visualização geográfica da exposição média à Inteligência Artificial
    nas ocupações brasileiras, com base nos dados agregados por estado.
    """)

    st.divider()

    # ======================================
    # VALIDAR COLUNAS
    # ======================================

    colunas_necessarias = ["UF", "AIOE_SCORE"]

    faltando = [
        col for col in colunas_necessarias
        if col not in df.columns
    ]

    if faltando:

        st.error(f"Colunas não encontradas: {faltando}")

        st.write("Colunas disponíveis:")
        st.write(df.columns.tolist())

        return

    # ======================================
    # LIMPEZA
    # ======================================

    mapa = df.dropna(
        subset=[
            "UF",
            "AIOE_SCORE"
        ]
    ).copy()

    # ======================================
    # PADRONIZAÇÃO
    # ======================================

    mapa["UF"] = (
        mapa["UF"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ======================================
    # ESTADOS -> SIGLAS
    # ======================================

    estados_siglas = {

        "ACRE": "AC",
        "ALAGOAS": "AL",
        "AMAPÁ": "AP",
        "AMAZONAS": "AM",
        "BAHIA": "BA",
        "CEARÁ": "CE",
        "DISTRITO FEDERAL": "DF",
        "ESPÍRITO SANTO": "ES",
        "GOIÁS": "GO",
        "MARANHÃO": "MA",
        "MATO GROSSO": "MT",
        "MATO GROSSO DO SUL": "MS",
        "MINAS GERAIS": "MG",
        "PARÁ": "PA",
        "PARAÍBA": "PB",
        "PARANÁ": "PR",
        "PERNAMBUCO": "PE",
        "PIAUÍ": "PI",
        "RIO DE JANEIRO": "RJ",
        "RIO GRANDE DO NORTE": "RN",
        "RIO GRANDE DO SUL": "RS",
        "RONDÔNIA": "RO",
        "RORAIMA": "RR",
        "SANTA CATARINA": "SC",
        "SÃO PAULO": "SP",
        "SERGIPE": "SE",
        "TOCANTINS": "TO"
    }

    # ======================================
    # CONVERTER
    # ======================================

    mapa["SIGLA"] = mapa["UF"].map(estados_siglas)

    mapa = mapa.dropna(subset=["SIGLA"])

    # ======================================
    # AGRUPAR
    # ======================================

    mapa = (
        mapa.groupby(
            ["UF", "SIGLA"]
        )["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    # ======================================
    # GEOJSON
    # ======================================

    try:

        with open(
            "data/brasil_estados.geojson",
            "r",
            encoding="utf-8"
        ) as f:

            brasil_geo = json.load(f)

    except Exception as e:

        st.error(f"Erro ao carregar GeoJSON: {e}")

        return

    # ======================================
    # MAPA
    # ======================================

    fig_mapa = px.choropleth(

        mapa,

        geojson=brasil_geo,

        locations="SIGLA",

        featureidkey="properties.sigla",

        color="AIOE_SCORE",

        color_continuous_scale="Reds",

        hover_name="UF",

        hover_data={
            "SIGLA": True,
            "AIOE_SCORE": ":.3f"
        },

        title="Mapa de Exposição Média à IA por Estado"
    )

    # ======================================
    # AJUSTES
    # ======================================

    fig_mapa.update_geos(

        fitbounds="locations",

        visible=False
    )

    fig_mapa.update_layout(

        height=850,

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        ),

        coloraxis_colorbar=dict(
            title="AIOE"
        )
    )

    # ======================================
    # EXIBIR
    # ======================================

    st.plotly_chart(
        fig_mapa,
        use_container_width=True
    )

    st.caption("""
    O mapa apresenta a média do score AIOE por estado brasileiro,
    permitindo visualizar diferenças regionais na exposição ocupacional
    à Inteligência Artificial.
    """)
