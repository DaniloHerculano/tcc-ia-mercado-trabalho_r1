import streamlit as st
import os

def mostrar_evolucao_temporal(df=None):
    st.title("📈 Séries Temporais e Dinâmica Demográfica de Gênero")
    st.markdown("Acompanhe as curvas da exposição à IA no mercado brasileiro (2020–2025).")
    st.divider()
    
    # Caminho absoluto blindado para a pasta img
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    img_dir = os.path.join(project_dir, "img")
    
    # -------------------------------------------------------------------------
    # SEÇÃO 1: EVOLUÇÃO LONGITUDINAL TRIMESTRAL
    # -------------------------------------------------------------------------
    st.subheader("1. Evolução Longitudinal Trimestral")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Evolução Trimestral — AIOE")
        st.image(os.path.join(img_dir, "evolucao-trimestral-AIOE.png"), use_container_width=True)
        
    with col2:
        st.markdown("#### Evolução Trimestral — Gmyrek")
        st.image(os.path.join(img_dir, "evolucao-trimestral-exposure.png"), use_container_width=True)

    st.divider()

    # -------------------------------------------------------------------------
    # SEÇÃO 2: RECORTE DE GÊNERO
    # -------------------------------------------------------------------------
    st.subheader("2. Recorte de Gênero na Exposição")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Evolução por Gênero — AIOE")
        st.image(os.path.join(img_dir, "evolucao-genero-aioe.png"), use_container_width=True)
        
    with col4:
        st.markdown("#### Evolução por Gênero — Gmyrek")
        st.image(os.path.join(img_dir, "evolucao-genero-exposure.png"), use_container_width=True)

    st.write("")

    # -------------------------------------------------------------------------
    # GRÁFICO 5: COMPOSIÇÃO DE GÊNERO
    # -------------------------------------------------------------------------
    st.markdown("#### 📊 Composição de Gênero por Faixas de Impacto (AIOE)")
    st.image(os.path.join(img_dir, "composicao-genero-AIOE.png"), use_container_width=True)
