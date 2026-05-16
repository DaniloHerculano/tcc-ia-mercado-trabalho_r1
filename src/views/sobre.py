import streamlit as st


# ==========================================
# SOBRE
# ==========================================

def mostrar_sobre():

    st.title(
        "ℹ️ Sobre o Projeto"
    )

    st.markdown("""
    ## TCC - Ciência de Dados

    Plataforma desenvolvida para análise
    do impacto da Inteligência Artificial
    no mercado de trabalho brasileiro.

    O projeto utiliza técnicas modernas
    de NLP (Processamento de Linguagem Natural),
    embeddings semânticos e similaridade de cosseno
    para relacionar ocupações brasileiras da CBO
    com ocupações internacionais do dataset AIOE.
    """)

    st.divider()

    # ======================================
    # METODOLOGIA
    # ======================================

    st.subheader(
        "🧠 Metodologia"
    )

    st.markdown("""
    ### Coleta de Dados

    - CBO (Classificação Brasileira de Ocupações)
    - PNAD Contínua
    - Dataset AIOE (Felten et al.)

    ### NLP e Embeddings

    - Sentence Transformers
    - Modelo multilingual-e5-large
    - Similaridade de Cosseno

    ### Processamento

    - OCR
    - Regex
    - Normalização textual
    - Matching semântico

    ### Visualização

    - Streamlit
    - Plotly
    - Pandas
    """)

    st.divider()

    # ======================================
    # TECNOLOGIAS
    # ======================================

    st.subheader(
        "⚙️ Tecnologias"
    )

    st.markdown("""
    - Python
    - Pandas
    - PyTorch
    - Sentence Transformers
    - Plotly
    - Streamlit
    - Parquet
    - OpenPyXL
    """)

    st.divider()

    # ======================================
    # OBJETIVO
    # ======================================

    st.subheader(
        "🎯 Objetivo"
    )

    st.info("""
    Identificar profissões e setores
    com maior potencial de impacto
    da Inteligência Artificial,
    permitindo análises sociais,
    econômicas e educacionais.
    """)