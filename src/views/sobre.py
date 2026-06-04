import streamlit as st


def mostrar_sobre():

    st.title("ℹ️ Sobre o Projeto")

    st.success("""
    🔬 **Trabalho de Conclusão de Curso (TCC) em Ciência de Dados — UNIVESP**

    Esta plataforma foi desenvolvida para mapear, mensurar e analisar a **exposição potencial das ocupações brasileiras à Inteligência Artificial**, integrando indicadores globais de exposição aos microdados de emprego nacionais.
    """)

    st.success("""
    **Contribuição do estudo**

    O principal resultado deste trabalho não consiste na criação de um novo modelo de Inteligência Artificial, mas na integração de bases ocupacionais nacionais e internacionais para analisar a exposição potencial das ocupações brasileiras às tecnologias de IA generativa.
    """)

    st.divider()

    # ==================================================
    # VISÃO GERAL
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🎯 O Diferencial Metodológico")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Registros Analisados", "≈ 1 milhão")
        m2.metric("Ocupações Mapeadas", "2.600+")
        m3.metric("Estados Brasileiros", "27")
        m4.metric("Período", "2020–2025")

        st.markdown("""
        Diferente de aplicações simples que utilizam apenas indicadores prontos, este projeto desenvolveu uma infraestrutura metodológica para compatibilizar dados ocupacionais nacionais e internacionais.

        Foram realizados experimentos utilizando embeddings e similaridade semântica como apoio ao processo de compatibilização ocupacional.

        Entretanto, os resultados apresentaram níveis moderados de correspondência e, por esse motivo, os indicadores finais utilizados nas análises foram obtidos prioritariamente por métodos estruturados de compatibilização entre classificações ocupacionais.
        """)

    with col2:

        st.subheader("📊 Bases de Dados Harmonizadas")

        st.markdown("""
        * **CBO (Classificação Brasileira de Ocupações):** Dados e descrições sumárias oficiais do Ministério do Trabalho.

        * **PNAD Contínua (IBGE):** Base abrangendo o período de **2020 a 2025**, totalizando aproximadamente **1 milhão de registros válidos** após o tratamento dos dados.

        * **Datasets Globais de IA:** Índice de Exposição Ocupacional à IA (**AIOE**) de Felten, Raj e Seamans (2023) e classificação de exposição potencial da OIT proposta por Gmyrek et al. (2025).
        """)

    st.divider()

    # ==================================================
    # TECNOLOGIAS
    # ==================================================

    st.subheader("⚙️ Engenharia de Dados e Tecnologias Adotadas")

    st.write(
        "Clique nas etapas abaixo para visualizar as principais tecnologias utilizadas no desenvolvimento do projeto."
    )

    with st.expander("🛠️ 1. Coleta, OCR e Pré-processamento"):

        st.markdown("""
        * **Extração e OCR:** Utilização das bibliotecas `pdfplumber`, `pytesseract` e `pdf2image` para extração de dados dos documentos oficiais da CBO.

        * **Limpeza e Padronização:** Uso de expressões regulares (`re`) para tratamento e padronização dos dados.

        * **Manipulação de Arquivos:** Processamento de planilhas e arquivos intermediários utilizando `openpyxl` e `xlrd`.
        """)

    with st.expander("🧠 2. NLP, Embeddings e Similaridade Semântica"):

        st.markdown("""
        * **Embeddings:** Testes realizados com o modelo `text-embedding-3-large` da OpenAI.

        * **Similaridade de Cosseno:** Aplicação de métricas de similaridade utilizando `scikit-learn`.

        * **Fuzzy Matching:** Utilização da biblioteca `rapidfuzz` para apoio na correspondência textual entre ocupações.

        * **Frameworks Utilizados:** `PyTorch` e `Sentence-Transformers`.
        """)

    with st.expander("💾 3. Processamento de Dados e Estatística"):

        st.markdown("""
        * **DuckDB:** Banco analítico utilizado para consultas e agregações sobre os dados da PNAD.

        * **Pandas e Apache Parquet:** Estrutura principal para armazenamento e manipulação dos dados.

        * **Tratamento de Outliers:** Aplicação de técnicas de winsorização para redução da influência de valores extremos.

        * **NumPy:** Utilizado para cálculos estatísticos e operações vetorizadas.
        """)

    with st.expander("🖥️ 4. Plataforma e Visualização"):

        st.markdown("""
        * **Streamlit:** Desenvolvimento da plataforma analítica interativa.

        * **Plotly:** Construção de gráficos e visualizações interativas.

        * **Python:** Linguagem utilizada para integração entre processamento, análise e visualização dos dados.
        """)

    st.divider()

    # ==================================================
    # LIMITAÇÕES
    # ==================================================

    st.warning("""
    **Limitações do estudo**

    • Os indicadores AIOE foram originalmente desenvolvidos para ocupações internacionais.

    • A aplicação ao contexto brasileiro foi realizada por meio de compatibilização ocupacional.

    • Os resultados devem ser interpretados como indicadores de exposição potencial à Inteligência Artificial e não como previsões de substituição de empregos.
    """)

    st.info("""
    **Observação metodológica**

    Os indicadores apresentados nesta plataforma representam medidas de exposição potencial à Inteligência Artificial obtidas a partir da compatibilização entre classificações ocupacionais nacionais e internacionais.

    Dessa forma, os resultados não devem ser interpretados como estimativas diretas de substituição de empregos, mas como uma aproximação do grau de exposição das atividades profissionais às tecnologias de IA.
    """)

    st.divider()

    # ==================================================
    # EQUIPE
    # ==================================================

    st.subheader("🎓 Integrantes do Projeto")

    st.caption(
        "Universidade Virtual do Estado de São Paulo (UNIVESP) | Bacharelado em Ciência de Dados"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        * CAMILA DO NASCIMENTO MOREIRA LIMA
        * CLAUDIA MARTINS GUIDARA
        * DANILO VALENTIM HERCULANO
        * FELIPE FERNANDES DELVECCHIO
        """)

    with col2:

        st.markdown("""
        * FERNANDA OLIVEIRA PIOTTO
        * LUIS FERNANDO DE JESUS SANTOS
        * MARCELO VILELA MADURO
        * RENATO REGIO DE ARAUJO
        """)

    st.info("👨‍🏫 **Orientador:** Prof. DAVID LUZ")

    st.info("""
    📚 **Grupo 6**

    Disciplina: **TCC530 – Trabalho de Conclusão de Curso em Ciência de Dados**

    Turma: **010**

    Ano: **2026**
    """)

    st.divider()

    # ==================================================
    # VÍDEO
    # ==================================================

    st.subheader("🎥 Vídeo de Apresentação")

    st.markdown("""
    Assista à apresentação oficial do projeto para conhecer os objetivos, a metodologia adotada, as bases de dados utilizadas e os principais resultados obtidos.
    """)

    youtube_url = "https://www.youtube.com/watch?v=VIDEO_PENDENTE_AGUARDAR"

    st.video(youtube_url)

    st.divider()

    # ==================================================
    # LINKS
    # ==================================================

    st.subheader("🔗 Links do Projeto")

    st.markdown(f"""
    **🌐 Plataforma Analítica**

    https://tcc-ia-mercado-trabalhor1-r1-grupo-6.streamlit.app/

    **💻 Repositório GitHub**

    https://github.com/DaniloHerculano/tcc-ia-mercado-trabalho_r1

    **🎥 Vídeo de Apresentação**

    {youtube_url}
    """)

    st.divider()

    st.caption("""
    Trabalho de Conclusão de Curso desenvolvido no âmbito do Bacharelado em Ciência de Dados da Universidade Virtual do Estado de São Paulo (UNIVESP).

    As análises apresentadas possuem finalidade acadêmica e científica.
    """)
