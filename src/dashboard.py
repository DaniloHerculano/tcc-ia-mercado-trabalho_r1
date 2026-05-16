import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="IA e Mercado de Trabalho",
    layout="wide"
)

# ==========================================
# CAMINHO DO ARQUIVO
# ==========================================

ARQUIVO_DADOS = "data/tabela_cbo_e5_large_final.xlsx"

# ==========================================
# CARREGAR DADOS
# ==========================================

@st.cache_data
def carregar_dados():

    if not os.path.exists(ARQUIVO_DADOS):

        st.error(
            f"Arquivo não encontrado: {ARQUIVO_DADOS}"
        )

        st.stop()

    df = pd.read_excel(
        ARQUIVO_DADOS
    )

    return df

df = carregar_dados()

# ==========================================
# TRATAMENTOS
# ==========================================

df.columns = (
    df.columns
    .str.strip()
)

df["AIOE_SCORE"] = pd.to_numeric(
    df["AIOE_SCORE"],
    errors="coerce"
)

df["CONFIDENCE_SCORE"] = pd.to_numeric(
    df["CONFIDENCE_SCORE"],
    errors="coerce"
)

# ==========================================
# CRIAR NÍVEL DE IMPACTO
# ==========================================

def classificar_impacto(score):

    if score >= 0.70:
        return "🔴 Alto"

    elif score >= 0.40:
        return "🟡 Médio"

    else:
        return "🟢 Baixo"

df["NIVEL_IMPACTO"] = (
    df["AIOE_SCORE"]
    .apply(classificar_impacto)
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Navegação")

pagina = st.sidebar.radio(
    "Selecione:",
    [
        "📊 Dashboard",
        "📋 Dados",
        "📈 Análises",
        "🏆 Ranking",
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
    Plataforma de análise do impacto da Inteligência Artificial
    nas ocupações brasileiras utilizando NLP,
    Embeddings e Similaridade Semântica.
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

    alto = len(
        df[df["NIVEL_IMPACTO"] == "🔴 Alto"]
    )

    medio = len(
        df[df["NIVEL_IMPACTO"] == "🟡 Médio"]
    )

    baixo = len(
        df[df["NIVEL_IMPACTO"] == "🟢 Baixo"]
    )

    col1, col2, col3 = st.columns(3)

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

    st.divider()

    col4, col5, col6, col7 = st.columns(4)

    col4.metric(
        "🔴 Alto Impacto",
        alto
    )

    col5.metric(
        "🟡 Médio Impacto",
        medio
    )

    col6.metric(
        "🟢 Baixo Impacto",
        baixo
    )

    col7.metric(
        "Confiança Média",
        media_conf
    )

    st.divider()

    # ======================================
    # FILTROS
    # ======================================

    colf1, colf2 = st.columns(2)

    with colf1:

        grupo = st.selectbox(
            "Grande Grupo",
            ["Todos"] +
            sorted(
                df["Grande Grupo"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

    with colf2:

        impacto = st.selectbox(
            "Nível de Impacto",
            [
                "Todos",
                "🔴 Alto",
                "🟡 Médio",
                "🟢 Baixo"
            ]
        )

    busca = st.text_input(
        "🔎 Buscar ocupação"
    )

    # ======================================
    # FILTRO DF
    # ======================================

    df_filtrado = df.copy()

    if grupo != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["Grande Grupo"]
            == grupo
        ]

    if impacto != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["NIVEL_IMPACTO"]
            == impacto
        ]

    if busca:

        df_filtrado = df_filtrado[
            df_filtrado["TITULO_LIMPO"]
            .astype(str)
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    st.divider()

    # ======================================
    # GRÁFICO
    # ======================================

    grafico = (
        df_filtrado["NIVEL_IMPACTO"]
        .value_counts()
        .reset_index()
    )

    grafico.columns = [
        "Impacto",
        "Quantidade"
    ]

    fig = px.bar(
        grafico,
        x="Impacto",
        y="Quantidade",
        color="Impacto",
        title="Distribuição dos Níveis de Impacto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # TOP 10
    # ======================================

    st.subheader(
        "🏆 Top 10 Ocupações com Maior Exposição à IA"
    )

    top10 = (
        df_filtrado
        .sort_values(
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
        .head(10)
    )

    st.dataframe(
        top10,
        use_container_width=True
    )

# ==========================================
# DADOS
# ==========================================

elif pagina == "📋 Dados":

    st.title("📋 Base de Dados")

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================================
# ANÁLISES
# ==========================================

elif pagina == "📈 Análises":

    st.title("📈 Análises")

    # ======================================
    # HISTOGRAMA
    # ======================================

    fig1 = px.histogram(
        df,
        x="AIOE_SCORE",
        nbins=30,
        title="Distribuição do Score AIOE"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ======================================
    # CONFIANÇA
    # ======================================

    fig2 = px.histogram(
        df,
        x="CONFIDENCE_SCORE",
        nbins=30,
        title="Distribuição da Confiança"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

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
        [
            [
                "TITULO_LIMPO",
                "Grande Grupo",
                "AIOE_SCORE",
                "AIOE_MATCH_TITLE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ]
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )

# ==========================================
# SOBRE
# ==========================================

elif pagina == "ℹ️ Sobre":

    st.title("ℹ️ Sobre o Projeto")

    st.markdown("""
    ## TCC - Ciência de Dados

    Projeto desenvolvido para análise do impacto
    da Inteligência Artificial nas ocupações brasileiras.

    ## Tecnologias Utilizadas

    - Python
    - Pandas
    - NLP
    - Sentence Transformers
    - Embeddings
    - Similaridade de Cosseno
    - Streamlit
    - Plotly

    ## Objetivo

    Identificar profissões com maior potencial
    de impacto/exposição à Inteligência Artificial
    utilizando análise semântica entre
    ocupações brasileiras e americanas.
    """)