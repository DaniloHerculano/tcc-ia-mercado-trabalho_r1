import streamlit as st
import os

def mostrar_impacto_brasil(df=None):
    st.title("🇧🇷 Impacto Econômico e Rankings no Mercado Brasileiro")
    st.markdown("""
    Resultados consolidados do impacto da IA no cenário nacional: a relação com a renda média 
    e os rankings das ocupações nos extremos do mercado.
    """)
    st.divider()
    
    # Caminho absoluto blindado para a pasta img (voltando de src/views/ para raiz/img/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    img_dir = os.path.join(project_dir, "img")
    
    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais (Top/Bottom 20)"])
    
    # -------------------------------------------------------------------------
    # ABA 1: DISPERSÃO E REGRESSÃO (IMAGENS ESTÁTICAS)
    # -------------------------------------------------------------------------
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Elasticidade Renda × Índice AIOE (Felten)")
            st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-AIOE.png"), use_container_width=True)
            
        with col2:
            st.markdown("#### Elasticidade Renda × Métrica Gmyrek (OIT)")
            st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-Gmyrek.png"), use_container_width=True)

    # -------------------------------------------------------------------------
    # ABA 2: RANKINGS EXTREMOS (IMAGENS ESTÁTICAS)
    # -------------------------------------------------------------------------
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição")
        
        modelo = st.radio("Selecione o referencial teórico:", ["Indicador AIOE", "Indicador Gmyrek / OIT"], horizontal=True)
        st.write("")
        
        col_t1, col_t2 = st.columns(2)
        
        if "AIOE" in modelo:
            with col_t1:
                st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
                st.image(os.path.join(img_dir, "top20-ocupacoes-br-AIOE.png"), use_container_width=True)
            with col_t2:
                st.markdown("#### 🟢 20 Ocupações Menos Expostas")
                st.image(os.path.join(img_dir, "20-ocupacoes-br-AIOE.png"), use_container_width=True)
        else:
            with col_t1:
                st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
                st.image(os.path.join(img_dir, "top20-ocupacoes-br-Gmyrek.png"), use_container_width=True)
            with col_t2:
                st.markdown("#### 🟢 20 Ocupações Menos Expostas")
                st.image(os.path.join(img_dir, "20-ocupacoes-br-Gmyrek.png"), use_container_width=True)
