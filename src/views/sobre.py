import streamlit as st

def mostrar_sobre():
    st.title("ℹ️ Sobre o Projeto")
    
    # Card de Introdução Direta
    st.success("""
    🔬 **Trabalho de Conclusão de Curso (TCC) em Ciência de Dados — UNIVESP** Esta plataforma foi desenvolvida para mapear, mensurar e analisar o **impacto socioeconômico da Inteligência Artificial no mercado de trabalho brasileiro**, integrando indicadores globais de exposição aos microdados de emprego nacionais.
    """)
    
    st.divider()

    # ==========================================
    # O PROJETO (Visão Geral Curta)
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 O Diferencial Metodológico")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Registros Analisados", "≈ 1 milhão")
        m2.metric("Ocupações Mapeadas", "2.600+")
        m3.metric("Estados Brasileiros", "27")
        m4.metric("Período", "2020–2025")

        st.markdown("""
        Diferente de aplicações simples que usam apenas scores prontos, este projeto construiu uma **infraestrutura metodológica de pesquisa ocupacional**. 
        
        Foram realizados experimentos utilizando embeddings e similaridade semântica para apoiar o processo de compatibilização ocupacional. Entretanto, devido aos níveis de similaridade observados, os resultados finais priorizaram métodos estruturados de correspondência ocupacional.
        """)
        
    with col2:
        st.subheader("📊 Bases de Dados Harmonizadas")
        st.markdown("""
        * **CBO (Classificação Brasileira de Ocupações)**: Dados e descrições sumárias oficiais do Ministério do Trabalho.
        * **Microdados da PNAD Contínua (IBGE)**: Painel analítico abrangendo de **2020 a 2025**, totalizando uma amostra limpa de quase **1 milhão de registros** únicos.
        * **Datasets Globais de IA:** Índice de Exposição Ocupacional à IA (AIOE) de **Felten, Raj e Seamans (2023)** e classificação de impacto da OIT (**Gmyrek et al., 2025**).
        """)

    st.divider()

    # ==========================================
    # TECNOLOGIAS E ETAPAS (Organizado por Expander para não cansar o usuário)
    # ==========================================
    st.subheader("⚙️ Engenharia de Dados e Tecnologias Adotadas")
    st.write("Clique nas etapas abaixo para expandir e visualizar as tecnologias e abordagens aplicadas:")

    with st.expander("🛠️ 1. Coleta, OCR e Pré-processamento"):
        st.markdown("""
        * **Extração e OCR:** Uso das bibliotecas `pdfplumber`, `pytesseract` e `pdf2image` (com Poppler) para extrair dados textuais estruturados diretamente dos livros oficiais em PDF da CBO.
        * **Limpeza e Padronização:** Expressões Regulares (`re`) para tratar ruídos sistemáticos de formatação, hifens e reconstruir códigos hierárquicos ocupacionais de até 6 dígitos.
        * **Motores de Arquivo:** Leitura e tratamento de matrizes intermediárias e planilhas com `openpyxl` e `xlrd`.
        """)

    with st.expander("🧠 2. NLP, Embeddings e Mapeamento Semântico"):
        st.markdown("""
        * **Modelos de Embeddings:** Migração estratégica do modelo open-source `intfloat/multilingual-e5-large`para a API de embeddings da OpenAI utilizando o modelo `text-embedding-3-large`.
        * **Algoritmo de Similaridade:** Aplicação de **Similaridade de Cosseno** via `scikit-learn` para resolver dados residuais onde não havia correspondência estrutural direta entre os dicionários de ocupações.
        * **Ajuste Fino Textual:** Implementação de técnicas de *Fuzzy Matching* com a biblioteca `rapidfuzz` para correção automatizada de variações ortográficas, plurais e grafias entre os títulos das vagas.
        * **Frameworks Base:** `PyTorch` e `Sentence-Transformers`.
        """)

    with st.expander("💾 3. Processamento de Dados, Estatística e Integração da PNAD"):
        st.markdown("""
        * **Mecanismo de Consulta:** Utilização do **`DuckDB`** como banco analítico em memória para realizar junções e agregações complexas nos Parquets trimestrais da PNAD, contornando gargalos de estouro de memória RAM.
        * **Armazenamento de Alta Performance:** Manipulação de Big Data utilizando `Pandas` integrado com formatos compactos **Apache Parquet** (`pyarrow` e `fastparquet`).
        * **Tratamento de Outliers:** Técnicas de **Winsorização** aplicadas via Pandas (`quantile` e `clip`) nas caudas salariais para neutralizar a influência de outliers na renda mensal ponderada.
        * **Cálculos Vetoriais:** Operações estatísticas, logaritmos de renda e médias ponderadas usando `NumPy` (`np.average`, `np.log`).
        """)

    with st.expander("🖥️ 4. Visualização e Interface da Plataforma"):
        st.markdown("""
        * **Framework Web:** Interface responsiva construída inteiramente em `Streamlit`.
        * **Gráficos Interativos:** Visualizações dinâmicas criadas com `Plotly Express` e `Plotly Graph Objects`, calibrados para evitar quebras em telas móveis e monitores horizontais.
        """)

    st.divider()

    st.warning("""
    Limitações do estudo:
    
    • Os indicadores AIOE foram originalmente desenvolvidos para ocupações internacionais.
    
    • A aplicação ao contexto brasileiro foi realizada por meio de compatibilização ocupacional.
    
    • Os resultados devem ser interpretados como indicadores de exposição potencial à IA e não como previsões de substituição de empregos.
    """)

    # ==========================================
    # INTEGRANTES E ORIENTAÇÃO (UNIVESP)
    # ==========================================
    st.subheader("🎓 Integrantes do Projeto")
    st.caption("Universidade Virtual do Estado de São Paulo — UNIVESP | Curso de Bacharelado em Ciência de Dados")
    
    # Organização dos integrantes em duas colunas
    int_col1, int_col2 = st.columns(2)
    
    with int_col1:
        st.markdown("""
        * CAMILA DO NASCIMENTO MOREIRA LIMA
        * CLAUDIA MARTINS GUIDARA
        * DANILO VALENTIM HERCULANO
        * FELIPE FERNANDES DELVECCHIO
        """)
        
    with int_col2:
        st.markdown("""
        * FERNANDA OLIVEIRA PIOTTO
        * LUIS FERNANDO DE JESUS SANTOS
        * MARCELO VILELA MADURO
        * RENATO REGIO DE ARAUJO
        """)

    st.write("")
    
    # Destaque para a Orientação do TCC
    st.info("👨‍🏫 **Orientador:** Prof. DAVID LUZ")

    # Destaque curso, disciplina, turma...
    st.info("""
    📚 **Grupo 6**  
    Disciplina: **Trabalho de Conclusão de Curso em Ciência de Dados — TCC530**  
    Turma: **010**  
    Ano: **2026**
    """)

    st.divider()

    # ==========================================
    # VÍDEO DE APRESENTAÇÃO
    # ==========================================
    st.subheader("🎥 Vídeo de Apresentação")

    st.markdown("""
    Assista à apresentação oficial do Trabalho de Conclusão de Curso, onde são apresentados os objetivos, metodologia, bases de dados, resultados obtidos e a plataforma analítica desenvolvida pelo Grupo 6.
    """)

    # Substitua pelo link oficial do vídeo
    youtube_url = "https://www.youtube.com/watch?v=VIDEO_PENDENTE_AGUARDAR..."

    st.video(youtube_url)

    st.divider()

    # ==========================================
    # LINKS DO PROJETO
    # ==========================================
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
