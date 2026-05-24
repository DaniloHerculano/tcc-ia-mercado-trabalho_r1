import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_evolucao_temporal(df):
    st.title("📈 Séries Temporais e Dinâmica Demográfica de Gênero")
    st.markdown("""
    Acompanhe de forma interativa a evolução histórica da exposição à Inteligência Artificial no mercado de trabalho brasileiro 
    entre os anos de **2020 e 2025**.
    """)
    
    st.divider()
    
    # Criando a linha de tempo combinando Ano e Trimestre (ex: 2020-T1, 2020-T2...)
    df_time = df.dropna(subset=["Ano", "Trimestre", "AIOE_SCORE", "CONFIDENCE_SCORE", "Sexo"]).copy()
    df_time["Periodo"] = df_time["Ano"].astype(str) + "-T" + df_time["Trimestre"].astype(str)
    
    # -------------------------------------------------------------------------
    # SEÇÃO 1: EVOLUÇÃO LONGITUDINAL GERAL
    # -------------------------------------------------------------------------
    st.subheader("1. Evolução Longitudinal Trimestral")
    
    df_linha_geral = df_time.groupby("Periodo").agg({
        "AIOE_SCORE": "mean",
        "CONFIDENCE_SCORE": "mean"
    }).reset_index()
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("#### Evolução Média do Índice AIOE")
        fig_l1 = px.line(df_linha_geral, x="Periodo", y="AIOE_SCORE", markers=True, color_discrete_sequence=["#1f77b4"])
        fig_l1.update_layout(height=380, xaxis_title="", yaxis_title="Média AIOE", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_l1, use_container_width=True)
        
    with col_t2:
        st.markdown("#### Evolução Média do Gradiente de Exposição (Gmyrek)")
        fig_l2 = px.line(df_linha_geral, x="Periodo", y="CONFIDENCE_SCORE", markers=True, color_discrete_sequence=["#ff7f0e"])
        fig_l2.update_layout(height=380, xaxis_title="", yaxis_title="Média Exposure", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_l2, use_container_width=True)
        
    st.divider()
    
    # -------------------------------------------------------------------------
    # SEÇÃO 2: RECORTE HISTÓRICO POR GÊNERO
    # -------------------------------------------------------------------------
    st.subheader("2. Assimetria de Gênero na Força de Trabalho")
    st.markdown("Acompanhe o descolamento das linhas de tendência de exposição histórica entre homens e mulheres:")
    
    df_linha_sexo = df_time.groupby(["Periodo", "Sexo"]).agg({
        "AIOE_SCORE": "mean",
        "CONFIDENCE_SCORE": "mean"
    }).reset_index()
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("#### Exposição por Gênero — Modelo AIOE")
        fig_s1 = px.line(df_linha_sexo, x="Periodo", y="AIOE_SCORE", color="Sexo", markers=True,
                         color_discrete_map={"Masculino": "#1f77b4", "Feminino": "#e377c2"})
        fig_s1.update_layout(height=380, xaxis_title="", yaxis_title="Média AIOE", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_s1, use_container_width=True)
        
    with col_g2:
        st.markdown("#### Exposição por Gênero — Modelo Gmyrek")
        fig_s2 = px.line(df_linha_sexo, x="Periodo", y="CONFIDENCE_SCORE", color="Sexo", markers=True,
                         color_discrete_map={"Masculino": "#ff7f0e", "Feminino": "#9467bd"})
        fig_s2.update_layout(height=380, xaxis_title="", yaxis_title="Média Exposure", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_s2, use_container_width=True)
        
    st.write("")
    
    # --- Gráfico Final de Densidade/Composição de Gênero por Faixas de Impacto ---
    st.markdown("#### 📊 Distribuição de Densidade Proporcional por Faixas de Score (Gênero)")
    
    # Definindo fatias de score para gerar o empilhamento dinâmico igual ao arquivo original
    df_time["Faixa_Score"] = pd.cut(df_time["AIOE_SCORE"], bins=[0, 0.3, 0.5, 0.7, 1.0], 
                                    labels=["0.0 a 0.3 (Baixo)", "0.3 a 0.5 (Moderado)", "0.5 a 0.7 (Médio)", "0.7 a 1.0 (Alto)"])
    
    df_comp = df_time.groupby(["Faixa_Score", "Sexo"]).size().reset_index(name="Quantidade")
    
    fig_comp = px.bar(
        df_comp, x="Faixa_Score", y="Quantidade", color="Sexo", 
        barmode="group", text_auto=True,
        labels={"Faixa_Score": "Faixas de Proximidade do Score AIOE", "Quantidade": "Volume Amostral Ponderado"},
        color_discrete_map={"Masculino": "#1f77b4", "Feminino": "#e377c2"}
    )
    fig_comp.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_comp, use_container_width=True)
