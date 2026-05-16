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
        "🇧🇷 Impacto no Brasil",
        "🎓 Escolaridade x IA",
        "💰 Renda x IA",
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
# IMPACTO NO BRASIL
# ==========================================

elif pagina == "🇧🇷 Impacto no Brasil":

    st.title(
        "🇧🇷 Impacto da IA no Brasil"
    )

    st.markdown("""
    Análise das ocupações brasileiras
    com base nos scores de exposição
    à Inteligência Artificial (AIOE).
    """)

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    total = len(df)

    media_aioe = round(
        df["AIOE_SCORE"].mean(),
        2
    )

    media_conf = round(
        df["CONFIDENCE_SCORE"].mean(),
        2
    )

    alto = len(
        df[df["NIVEL_IMPACTO"] == "🔴 Alto"]
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
        "Confiança Média",
        media_conf
    )

    col4.metric(
        "Alto Impacto",
        alto
    )

    st.divider()

    # ======================================
    # DISTRIBUIÇÃO IMPACTO
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

    fig = px.pie(
        impacto,
        names="Impacto",
        values="Quantidade",
        title="Distribuição de Impacto IA"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

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
                "AIOE_SCORE",
                "CONFIDENCE_SCORE",
                "NIVEL_IMPACTO"
            ]
        ]
        .head(15)
    )

    st.dataframe(
        top,
        width='stretch'
    )

    st.divider()

    # ======================================
    # GRANDES GRUPOS
    # ======================================

    st.subheader(
        "📊 Média AIOE por Grande Grupo"
    )

    grupo = (
        df.groupby("Grande Grupo")
        ["AIOE_SCORE"]
        .mean()
        .reset_index()
    )

    grupo = grupo.sort_values(
        by="AIOE_SCORE",
        ascending=False
    )

    fig2 = px.bar(
        grupo,
        x="Grande Grupo",
        y="AIOE_SCORE",
        color="AIOE_SCORE",
        title="Exposição Média por Grande Grupo"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

# ==========================================
# ESCOLARIDADE X IA
# ==========================================

elif pagina == "🎓 Escolaridade x IA":

    st.title(
        "🎓 Escolaridade x Impacto IA"
    )

    st.markdown("""
    Relação entre escolaridade
    e exposição à Inteligência Artificial.
    """)

    st.divider()

    # ======================================
    # AGRUPAMENTO
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
        title="Média de Exposição IA por Formação"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    st.divider()

    # ======================================
    # IMPACTO
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
        title="Distribuição de Impacto por Formação"
    )

    st.plotly_chart(
        fig2,
        width='stretch'
    )

    st.divider()

    # ======================================
    # TABELA
    # ======================================

    st.subheader(
        "📋 Dados Agrupados"
    )

    st.dataframe(
        escolaridade,
        width='stretch'
    )

    st.divider()

    # ======================================
    # INSIGHTS
    # ======================================

    maior = escolaridade.iloc[0]

    menor = escolaridade.iloc[-1]

    st.info(f"""
    🎓 Formação mais exposta:
    {maior['FORMAÇÃO E EXPERIÊNCIA']}

    Média AIOE:
    {round(maior['AIOE_SCORE'], 2)}
    """)

    st.success(f"""
    📘 Formação menos exposta:
    {menor['FORMAÇÃO E EXPERIÊNCIA']}

    Média AIOE:
    {round(menor['AIOE_SCORE'], 2)}
    """)

# ==========================================
# RENDA X IA
# ==========================================

elif pagina == "💰 Renda x IA":

    st.title(
        "💰 Renda x Impacto IA"
    )

    st.markdown("""
    Relação entre exposição à IA
    e níveis salariais.
    """)

    st.divider()

    # ======================================
    # FAIXAS SALARIAIS
    # ======================================

    if "RENDA_MEDIA" in df.columns:

        df_renda = df.copy()

        df_renda["FAIXA_RENDA"] = pd.cut(
            df_renda["RENDA_MEDIA"],
            bins=[0, 2000, 5000, 10000, 20000, 50000],
            labels=[
                "Até 2k",
                "2k-5k",
                "5k-10k",
                "10k-20k",
                "20k+"
            ]
        )

        # ==================================
        # MÉDIA AIOE
        # ==================================

        renda_media = (
            df_renda.groupby("FAIXA_RENDA")
            ["AIOE_SCORE"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            renda_media,
            x="FAIXA_RENDA",
            y="AIOE_SCORE",
            color="AIOE_SCORE",
            title="Média de Exposição IA por Faixa Salarial"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

        st.divider()

        # ==================================
        # DISTRIBUIÇÃO
        # ==================================

        impacto = (
            df_renda.groupby(
                [
                    "FAIXA_RENDA",
                    "NIVEL_IMPACTO"
                ]
            )
            .size()
            .reset_index(name="Quantidade")
        )

        fig2 = px.bar(
            impacto,
            x="FAIXA_RENDA",
            y="Quantidade",
            color="NIVEL_IMPACTO",
            barmode="group",
            title="Impacto IA por Faixa Salarial"
        )

        st.plotly_chart(
            fig2,
            width='stretch'
        )

        st.divider()

        # ==================================
        # TABELA
        # ==================================

        st.subheader(
            "📋 Média de Exposição"
        )

        st.dataframe(
            renda_media,
            width='stretch'
        )

        st.divider()

        # ==================================
        # INSIGHTS
        # ==================================

        maior = renda_media.sort_values(
            by="AIOE_SCORE",
            ascending=False
        ).iloc[0]

        menor = renda_media.sort_values(
            by="AIOE_SCORE",
            ascending=True
        ).iloc[0]

        st.warning(f"""
        💰 Faixa salarial mais exposta:

        {maior['FAIXA_RENDA']}

        Média AIOE:
        {round(maior['AIOE_SCORE'], 2)}
        """)

        st.success(f"""
        📉 Faixa salarial menos exposta:

        {menor['FAIXA_RENDA']}

        Média AIOE:
        {round(menor['AIOE_SCORE'], 2)}
        """)

    else:

        st.error(
            "Coluna RENDA_MEDIA não encontrada."
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