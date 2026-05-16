import streamlit as st
import pandas as pd
import plotly.express as px

from carregar_dados import (
    carregar_cbo,
    limpar_dados
)

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IA e Mercado de Trabalho",
    layout="wide"
)

# ==========================================
# CARREGAR DADOS
# ==========================================

@st.cache_data
def carregar():

    df = carregar_cbo()

    df = limpar_dados(df)

    return df


df = carregar()

# ==========================================
# MENU
# ==========================================

st.sidebar.title("📌 Navegação")

pagina = st.sidebar.radio(
    "Selecione:",
    [
        "📊 Dashboard",
        "🔎 Pesquisar Ocupação",
        "🏆 Ranking",
        "🧠 Similaridade",
        "ℹ️ Sobre"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if pagina == "📊 Dashboard":

    st.title(
        "🤖 IA e Mercado de Trabalho"
    )

    st.markdown("""
    Plataforma de análise do impacto da
    Inteligência Artificial nas ocupações
    brasileiras utilizando NLP, embeddings
    semânticos e similaridade de cosseno.
    """)

    # ======================================
    # MÉTRICAS
    # ======================================

    total = len(df)

    media_aioe = round(
        df["AIOE_SCORE"].mean(),
        2
    )

    max_aioe = round(
        df["AIOE_SCORE"].max(),
        2
    )

    media_conf = round(
        df["CONFIDENCE_SCORE"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total de Ocupações",
        total
    )

    col2.metric(
        "Média AIOE",
        media_aioe
    )

    col3.metric(
        "Maior Score",
        max_aioe
    )

    col4.metric(
        "Confiança Média",
        media_conf
    )

    st.divider()

    # ======================================
    # IMPACTO
    # ======================================

    impacto = (
        df["NIVEL_IMPACTO"]
        .value_counts()
        .reset_index()
    )

    impacto.columns = [
        "Impacto",
        "Quantidade"
    ]

    fig = px.bar(
        impacto,
        x="Impacto",
        y="Quantidade",
        color="Impacto",
        title="Distribuição de Impacto"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TOP 10
    # ======================================

    st.subheader(
        "🔥 Ocupações Mais Expostas"
    )

    top10 = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "CBO_EXTRAIDO",
                "TITULO_LIMPO",
                "AIOE_SCORE",
                "CONFIDENCE_SCORE"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        top10,
        width='stretch'
    )

# ==========================================
# PESQUISA DE OCUPAÇÃO
# ==========================================

elif pagina == "🔎 Pesquisar Ocupação":

    st.title(
        "🔎 Pesquisa de Ocupações"
    )

    st.markdown("""
    Consulte ocupações brasileiras
    e visualize o nível de exposição
    à Inteligência Artificial.
    """)

    # ======================================
    # BUSCA
    # ======================================

    busca = st.text_input(
        "Digite uma ocupação"
    )

    # ======================================
    # FILTRO IMPACTO
    # ======================================

    filtro = st.selectbox(
        "Filtrar impacto",
        [
            "Todos",
            "🔴 Alto",
            "🟡 Médio",
            "🟢 Baixo"
        ]
    )

    # ======================================
    # BASE FILTRADA
    # ======================================

    resultado = df.copy()

    if filtro != "Todos":

        resultado = resultado[
            resultado["NIVEL_IMPACTO"]
            == filtro
        ]

    if busca:

        resultado = resultado[
            resultado["TITULO_LIMPO"]
            .astype(str)
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    st.divider()

    st.write(
        f"{len(resultado)} ocupações encontradas."
    )

    # ======================================
    # RESULTADOS
    # ======================================

    for _, row in resultado.head(20).iterrows():

        st.markdown(f"""
        ---
        ### {row['TITULO_LIMPO']}

        **CBO:** {row['CBO_EXTRAIDO']}

        **Impacto IA:** {row['NIVEL_IMPACTO']}

        **AIOE Score:** {round(row['AIOE_SCORE'], 2)}

        **Confiança:** {round(row['CONFIDENCE_SCORE'], 2)}

        **Match AIOE:** {row['AIOE_MATCH_TITLE']}

        **Grande Grupo:** {row['Grande Grupo']}
        """)

# ==========================================
# RANKING
# ==========================================

elif pagina == "🏆 Ranking":

    st.title(
        "🏆 Ranking Geral"
    )

    ranking = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
    )

    st.dataframe(
        ranking[
            [
                "CBO_EXTRAIDO",
                "TITULO_LIMPO",
                "Grande Grupo",
                "AIOE_SCORE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ],
        width='stretch'
    )

# ==========================================
# SIMILARIDADE
# ==========================================

elif pagina == "🧠 Similaridade":

    st.title(
        "🧠 Similaridade Semântica"
    )

    st.markdown("""
    Correspondência semântica entre
    ocupações brasileiras (CBO)
    e ocupações americanas
    do dataset AIOE/Felten.
    """)

    tabela = df[
        [
            "TITULO_LIMPO",
            "AIOE_MATCH_TITLE",
            "CONFIDENCE_SCORE",
            "AIOE_SCORE"
        ]
    ]

    st.dataframe(
        tabela,
        width='stretch'
    )

# ==========================================
# SOBRE
# ==========================================

elif pagina == "ℹ️ Sobre":

    st.title("ℹ️ Sobre")

    st.markdown("""
    ### TCC - Ciência de Dados

    Projeto voltado para análise
    do impacto da Inteligência Artificial
    no mercado de trabalho brasileiro.

    ### Metodologia

    - NLP
    - Embeddings Semânticos
    - Similaridade de Cosseno
    - Sentence Transformers
    - Dataset AIOE (Felten et al.)
    - CBO Brasileira
    - PNAD Contínua

    ### Tecnologias

    - Python
    - Streamlit
    - Pandas
    - Plotly
    - PyTorch
    - Sentence Transformers
    """)