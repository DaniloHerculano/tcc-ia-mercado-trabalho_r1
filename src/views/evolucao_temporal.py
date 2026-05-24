import streamlit as st

def mostrar_evolucao_temporal(df):
    st.title("📈 Séries Temporais e Dinâmica Demográfica de Gênero")
    st.markdown("""
    Acompanhe a evolução histórica da exposição à Inteligência Artificial no mercado de trabalho brasileiro 
    entre os anos de **2020 e 2025**, detalhando o comportamento trimestral e os impactos assimétricos por sexo.
    """)
    
    st.divider()
    
    # SEÇÃO 1: EVOLUÇÃO TRIMESTRAL
    st.subheader("1. Evolução Longitudinal Trimestral")
    st.markdown("""
    Os painéis abaixo exibem o comportamento das médias gerais de exposição expandidas pelos pesos amostrais da PNAD. 
    Eles refletem flutuações estruturais na contratação e na composição do mercado ativo pós-pandemia.
    """)
    
    col_time1, col_time2 = st.columns(2)
    with col_time1:
        st.markdown("#### Linha Histórica de Médias — Modelo AIOE")
        st.image("evolucao-trimestral-AIOE.png", use_container_width=True)
    with col_time2:
        st.markdown("#### Linha Histórica de Médias — Modelo Gmyrek (Exposure)")
        st.image("evolucao-trimestral-exposure.png", use_container_width=True)
        
    st.divider()
    
    # SEÇÃO 2: ASSIMETRIA DE GÊNERO
    st.subheader("2. Recorte de Gênero na Exposição Tecnológica")
    st.markdown("""
    A literatura econômica aponta que a automação cognitiva tende a afetar de forma desigual a força de trabalho de acordo com o sexo, 
    uma vez que mulheres e homens ocupam proporções diferentes em setores de suporte administrativo e operacionais.
    """)
    
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        st.markdown("#### Tendência Histórica por Sexo — AIOE")
        st.image("evolucao-genero-aioe.png", use_container_width=True)
    with col_gen2:
        st.markdown("#### Tendência Histórica por Sexo — Gmyrek")
        st.image("evolucao-genero-exposure.png", use_container_width=True)
        
    st.write("")
    
    # Gráfico final de composição proporcional enviado por último
    st.markdown("#### 📊 Distribuição Proporcional da Força de Trabalho por Faixas de Impacto e Gênero")
    st.write("Visão agregada que expõe de forma estática a disparidade da densidade masculina e feminina nas faixas críticas de score:")
    st.image("composicao-genero-AIOE.png", use_container_width=True)
    
    st.caption("*Nota Metodológica: Todas as curvas temporais e distribuições utilizam as variáveis de projeção populacional (`Peso_Amostral`) fornecidas pelo IBGE.*")
