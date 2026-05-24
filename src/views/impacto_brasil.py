import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np  # <-- Faltava esse cara aqui!

def mostrar_impacto_brasil(df):
    st.title("🇧🇷 Impacto Econômico e Rankings no Mercado Brasileiro")
    st.markdown("""
    Nesta seção, exploramos de forma dinâmica a relação entre a remuneração dos trabalhadores 
    e sua exposição à IA, além dos rankings das profissões nos extremos do mercado.
    """)
    
    st.divider()
    
    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais (Top/Bottom 20)"])
    
    # -------------------------------------------------------------------------
    # ABA 1: DISPERSÃO E REGRESSÃO (RENDA)
    # -------------------------------------------------------------------------
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")
        st.markdown("Ajuste de tendência linear estimado diretamente sobre a amostragem de salários ponderados da PNAD:")
        
        # Preparando dados para evitar problemas de log(0) e NaNs
        df_renda = df.dropna(subset=["Rendimento_Mensal", "AIOE_SCORE", "CONFIDENCE_SCORE"]).copy()
        df_renda = df_renda[df_renda["Rendimento_Mensal"] > 0]
        df_renda["Log_Renda"] = np.log10(df_renda["Rendimento_Mensal"])
        
        # Agrupando por ocupação para gerar o gráfico de dispersão por profissão
        df_agrupado = df_renda.groupby("TITULO_LIMPO").agg({
            "Log_Renda": "mean",
            "AIOE_SCORE": "mean",
            "CONFIDENCE_SCORE": "mean" # Gradiente Gmyrek (Mean)
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Elasticidade Renda × Índice AIOE (Felten)")
            fig_r1 = px.scatter(
                df_agrupado, x="Log_Renda", y="AIOE_SCORE", 
                trendline="ols", hover_name="TITULO_LIMPO",
                labels={"Log_Renda": "Log10(Rendimento Mensal)", "AIOE_SCORE": "Score AIOE"},
                color_continuous_scale="Blues"
            )
            fig_r1.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_r1, use_container_width=True)
            
        with col2:
            st.markdown("#### Elasticidade Renda × Métrica Gmyrek (OIT)")
            fig_r2 = px.scatter(
                df_agrupado, x="Log_Renda", y="CONFIDENCE_SCORE", 
                trendline="ols", hover_name="TITULO_LIMPO",
                labels={"Log_Renda": "Log10(Rendimento Mensal)", "CONFIDENCE_SCORE": "Gradiente de Exposição (Mean)"},
                color_discrete_sequence=["#ef553b"]
            )
            fig_r2.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_r2, use_container_width=True)

    # -------------------------------------------------------------------------
    # ABA 2: RANKINGS EXTREMOS (TOP & BOTTOM 20)
    # -------------------------------------------------------------------------
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição no Universo CBO")
        
        modelo_ranking = st.radio(
            "Selecione a métrica do ranking:",
            ["Indicador AIOE (Felten et al.)", "Indicador de Exposição (Gmyrek / OIT)"],
            horizontal=True
        )
        
        # Extraindo os extremos reais baseados no DataFrame unificado
        if "AIOE" in modelo_ranking:
            df_rank = df.groupby("TITULO_LIMPO")["AIOE_SCORE"].first().reset_index()
            col_score = "AIOE_SCORE"
        else:
            df_rank = df.groupby("TITULO_LIMPO")["CONFIDENCE_SCORE"].first().reset_index()
            col_score = "CONFIDENCE_SCORE"
            
        top_20 = df_rank.sort_values(by=col_score, ascending=False).head(20)
        bottom_20 = df_rank.sort_values(by=col_score, ascending=True).head(20)
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
            fig_top = px.bar(
                top_20, x=col_score, y="TITULO_LIMPO", orientation="h",
                text_auto=".2f", color=col_score, color_continuous_scale="Reds"
            )
            fig_top.update_layout(height=600, yaxis={'categoryorder':'total ascending'}, showlegend=False, margin=dict(l=10, r=40, t=10, b=10))
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col_g2:
            st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
            fig_bot = px.bar(
                bottom_20, x=col_score, y="TITULO_LIMPO", orientation="h",
                text_auto=".2f", color=col_score, color_continuous_scale="Greens_r"
            )
            fig_bot.update_layout(height=600, yaxis={'categoryorder':'total descending'}, showlegend=False, margin=dict(l=10, r=40, t=10, b=10))
            st.plotly_chart(fig_bot, use_container_width=True)
