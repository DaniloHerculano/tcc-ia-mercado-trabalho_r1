import streamlit as st
import plotly.express as px
import pandas as pd
import os

def mostrar_impacto_brasil(df=None):
    st.title("🇧🇷 Impacto Econômico e Rankings no Mercado Brasileiro")
    st.markdown("""
    Resultados consolidados do impacto da IA no cenário nacional: a relação com a renda média 
    e os rankings das ocupações nos extremos do mercado.
    """)
    st.divider()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    img_dir = os.path.join(project_dir, "img")
    
    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais (Top/Bottom 20)"])
    
    # =========================================================================
    # ABA 1: DISPERSÃO E REGRESSÃO (IMAGENS ESTÁTICAS - Muito complexo copiar à mão)
    # =========================================================================
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Elasticidade Renda × Índice AIOE (Felten)")
            st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-AIOE.png"), use_container_width=True)
        with col2:
            st.markdown("#### Elasticidade Renda × Métrica Gmyrek (OIT)")
            st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-Gmyrek.png"), use_container_width=True)

    # =========================================================================
    # ABA 2: RANKINGS EXTREMOS (GRÁFICOS INTERATIVOS PLOTLY)
    # =========================================================================
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição")
        modelo = st.radio("Selecione o referencial teórico:", ["Indicador AIOE", "Indicador Gmyrek / OIT"], horizontal=True)
        st.write("")
        
        col_t1, col_t2 = st.columns(2)
        
        if "AIOE" in modelo:
            # ⬇️ COLOQUE AQUI OS SEUS DADOS REAIS DO TOP 20 AIOE ⬇️
            df_top = pd.DataFrame([
                {"Ocupação": "Profissão Exemplo 1", "Score": 0.95},
                {"Ocupação": "Profissão Exemplo 2", "Score": 0.90},
                # ... adicione as 20 aqui ...
                {"Ocupação": "Profissão Exemplo 20", "Score": 0.70}
            ])
            
            # ⬇️ COLOQUE AQUI OS SEUS DADOS REAIS DO BOTTOM 20 AIOE ⬇️
            df_bot = pd.DataFrame([
                {"Ocupação": "Profissão Exemplo A", "Score": 0.05},
                {"Ocupação": "Profissão Exemplo B", "Score": 0.10},
                # ... adicione as 20 aqui ...
                {"Ocupação": "Profissão Exemplo T", "Score": 0.30}
            ])
            
            escala_top, escala_bot = "Reds", "Greens_r"
            x_col = "Score"

        else:
            # ⬇️ COLOQUE AQUI OS SEUS DADOS REAIS DO TOP 20 GMYREK ⬇️
            df_top = pd.DataFrame([
                {"Ocupação": "Profissão Exemplo 1", "Score": 0.85},
                {"Ocupação": "Profissão Exemplo 2", "Score": 0.82},
                # ... adicione as 20 aqui ...
                {"Ocupação": "Profissão Exemplo 20", "Score": 0.60}
            ])
            
            # ⬇️ COLOQUE AQUI OS SEUS DADOS REAIS DO BOTTOM 20 GMYREK ⬇️
            df_bot = pd.DataFrame([
                {"Ocupação": "Profissão Exemplo A", "Score": 0.02},
                {"Ocupação": "Profissão Exemplo B", "Score": 0.04},
                # ... adicione as 20 aqui ...
                {"Ocupação": "Profissão Exemplo T", "Score": 0.20}
            ])
            
            escala_top, escala_bot = "Oranges", "Purples_r"
            x_col = "Score"

        # --- RENDERIZAÇÃO INTERATIVA PLOTLY ---
        with col_t1:
            st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
            # Ordenar para o gráfico ficar bonito
            df_top = df_top.sort_values(by=x_col, ascending=True)
            
            fig_top = px.bar(
                df_top, x=x_col, y="Ocupação", orientation="h", 
                text_auto=".2f", color=x_col, color_continuous_scale=escala_top
            )
            fig_top.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col_t2:
            st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
            # Ordenar para o gráfico ficar bonito
            df_bot = df_bot.sort_values(by=x_col, ascending=False)
            
            fig_bot = px.bar(
                df_bot, x=x_col, y="Ocupação", orientation="h", 
                text_auto=".2f", color=x_col, color_continuous_scale=escala_bot
            )
            fig_bot.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_bot, use_container_width=True)
