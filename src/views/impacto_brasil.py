import streamlit as st

def mostrar_impacto_brasil(df):
    st.title("🇧🇷 Impacto Econômico e Rankings no Mercado Brasileiro")
    st.markdown("""
    Nesta seção, exploramos os resultados substantivos do TCC: a relação entre a remuneração 
    dos trabalhadores e sua exposição à IA, além dos rankings das profissões mais e menos afetadas.
    """)
    
    st.divider()
    
    # Criação de abas para organizar o conteúdo de forma limpa
    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais (Top/Bottom 20)"])
    
    # -------------------------------------------------------------------------
    # ABA 1: ANÁLISE DE RENDA
    # -------------------------------------------------------------------------
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")
        st.markdown("""
        Os gráficos de dispersão abaixo apresentam as retas de regressão linear calculadas sobre os microdados da PNAD Contínua. 
        Eles testam a hipótese central de que a IA generativa impacta predominantemente ocupações de maior remuneração.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Modelo de Regressão — Métrica AIOE (Felten)")
            st.image("exposicao-ia-vs-log-renda-AIOE.png", use_container_width=True)
            st.caption("*Reta de tendência com inclinação positiva indicando maior exposição no topo salarial.*")
            
        with col2:
            st.markdown("#### Modelo de Regressão — Métrica Exposure (Gmyrek/OIT)")
            st.image("exposicao-ia-vs-log-renda-Gmyrek.png", use_container_width=True)
            st.caption("*Validação convergente utilizando o gradiente de tarefas expostas da OIT.*")
            
        st.info("""
        💡 **Análise Científica para o Relatório:** A inclinação positiva das retas em ambos os modelos confirma 
        estatisticamente que, no mercado brasileiro, as ocupações com maiores salários médios (ligadas ao setor de 
        tecnologia, finanças, gestão e administrativo) concentram o maior potencial de transformação tecnológica.
        """)

    # -------------------------------------------------------------------------
    # ABA 2: RANKINGS
    # -------------------------------------------------------------------------
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição no Universo CBO")
        st.markdown("Escolha o modelo metodológico abaixo para visualizar quais profissões ocupam os extremos da amostragem:")
        
        modelo_ranking = st.radio(
            "Selecione o referencial teórico:",
            ["Indicador AIOE (Felten et al.)", "Indicador de Exposição (Gmyrek / OIT)"],
            horizontal=True
        )
        
        st.write("")
        
        if "AIOE" in modelo_ranking:
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
                st.image("top20-ocupacoes-br-AIOE.png", use_container_width=True)
            with col_t2:
                st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
                st.image("bottom20-ocupacoes-br-AIOE.png", use_container_width=True)
            st.caption("*Fonte: Autores do TCC (Mapeamento baseado em Felten et al.).*")
        else:
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
                st.image("top20-ocupacoes-br-Gmyrek.png", use_container_width=True)
            with col_g2:
                st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
                st.image("bottom20-ocupacoes-br-Gmyrek.png", use_container_width=True)
            st.caption("*Fonte: Autores do TCC (Mapeamento baseado nos critérios de tarefas da OIT).*")
