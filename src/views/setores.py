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

    st.info("""
    O mapa apresenta a distribuição geográfica da exposição ocupacional à Inteligência Artificial no Brasil.
    
    Para cada estado foi calculada a média dos indicadores AIOE das ocupações presentes na base analisada. Valores mais elevados indicam maior concentração de ocupações potencialmente impactadas por tecnologias de IA generativa, enquanto valores menores sugerem predominância de atividades menos suscetíveis à automação baseada em conhecimento.
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

    # ======================================
    # RANKING DOS ESTADOS
    # ======================================
    
    st.subheader("🏆 Ranking dos Estados por Exposição Média à IA")
    
    ranking_estados = (
        mapa
        .sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        .reset_index(drop=True)
    )
    
    ranking_estados.index = ranking_estados.index + 1
    
    ranking_estados = ranking_estados.rename(
        columns={
            "UF": "Estado",
            "SIGLA": "UF",
            "AIOE_SCORE": "Score Médio AIOE"
        }
    )
    
    st.dataframe(
        ranking_estados,
        use_container_width=True
    )
    
    top5 = ranking_estados.head(5)
       
    st.success("""
    Interpretação:
    
    Diferenças entre estados não significam necessariamente maior ou menor adoção de Inteligência Artificial, mas refletem a composição ocupacional predominante em cada região.
    
    Estados com maior participação de atividades administrativas, financeiras, técnicas, científicas e de serviços intensivos em informação tendem a apresentar indicadores médios mais elevados. Já regiões com maior concentração de atividades operacionais, industriais, agrícolas ou manuais costumam apresentar níveis médios menores de exposição.
    """)

    # ======================================
    # MÉTRICAS NACIONAIS
    # ======================================
    
    media_nacional = mapa["AIOE_SCORE"].mean()
    
    estado_maior = mapa.loc[
        mapa["AIOE_SCORE"].idxmax()
    ]
    
    estado_menor = mapa.loc[
        mapa["AIOE_SCORE"].idxmin()
    ]
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric(
        "Média Nacional",
        f"{media_nacional:.3f}"
    )
    
    col2.metric(
        "Maior Exposição",
        estado_maior["SIGLA"]
    )
    
    col3.metric(
        "Menor Exposição",
        estado_menor["SIGLA"]
    )
    
    st.caption("""
    O mapa apresenta a média do score AIOE por estado brasileiro,
    permitindo visualizar diferenças regionais na exposição ocupacional
    à Inteligência Artificial.
    """)

    st.info(f"""
    Resumo dos resultados:
    
    • Exposição média nacional: {media_nacional:.3f}
    
    • Estado com maior exposição média: {estado_maior['UF']}
    
    • Estado com menor exposição média: {estado_menor['UF']}
    
    Esses resultados permitem identificar padrões regionais na distribuição das ocupações mais suscetíveis ao impacto da Inteligência Artificial, contribuindo para análises de desigualdade regional, qualificação profissional e planejamento de políticas públicas voltadas ao futuro do trabalho.
""")
