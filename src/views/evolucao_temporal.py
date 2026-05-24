import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_evolucao_temporal(df=None):
    st.title("📈 Séries Temporais e Dinâmica Demográfica de Gênero")
    st.markdown("Acompanhe as curvas interativas da exposição à IA no mercado brasileiro (2020–2025).")
    st.divider()
    
    # Períodos do eixo X idênticos aos das imagens
    periodos = ["2020-T1", "2020-T3", "2021-T1", "2021-T3", "2022-T1", "2022-T3", 
                "2023-T1", "2023-T3", "2024-T1", "2024-T3", "2025-T1"]
    
    # -------------------------------------------------------------------------
    # SEÇÃO 1: EVOLUÇÃO LONGITUDINAL TRIMESTRAL
    # -------------------------------------------------------------------------
    st.subheader("1. Evolução Longitudinal Trimestral")
    
    df_linhas = pd.DataFrame({
        "Período": periodos,
        "AIOE": [0.60, 0.605, 0.61, 0.612, 0.615, 0.618, 0.62, 0.625, 0.628, 0.63, 0.635],
        "Gmyrek": [0.33, 0.335, 0.338, 0.34, 0.342, 0.345, 0.348, 0.35, 0.352, 0.355, 0.36]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Evolução Trimestral — AIOE")
        fig1 = px.line(df_linhas, x="Período", y="AIOE", markers=True, color_discrete_sequence=["#1f77b4"])
        fig1.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.markdown("#### Evolução Trimestral — Gmyrek")
        fig2 = px.line(df_linhas, x="Período", y="Gmyrek", markers=True, color_discrete_sequence=["#ff7f0e"])
        fig2.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # -------------------------------------------------------------------------
    # SEÇÃO 2: RECORTE DE GÊNERO (LINHAS PARALELAS)
    # -------------------------------------------------------------------------
    st.subheader("2. Recorte de Gênero na Exposição")
    
    # Simulando o paralelismo: Feminino consistentemente acima do masculino
    df_sexo = pd.DataFrame([
        {"Período": p, "Sexo": "Feminino", "AIOE": a + 0.04, "Gmyrek": e + 0.03} for p, a, e in zip(periodos, df_linhas["AIOE"], df_linhas["Gmyrek"])
    ] + [
        {"Período": p, "Sexo": "Masculino", "AIOE": a - 0.03, "Gmyrek": e - 0.02} for p, a, e in zip(periodos, df_linhas["AIOE"], df_linhas["Gmyrek"])
    ])
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Evolução por Gênero — AIOE")
        fig3 = px.line(df_sexo, x="Período", y="AIOE", color="Sexo", markers=True, color_discrete_map={"Masculino": "#1f77b4", "Feminino": "#e377c2"})
        fig3.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig3, use_container_width=True)
        
    with col4:
        st.markdown("#### Evolução por Gênero — Gmyrek")
        fig4 = px.line(df_sexo, x="Período", y="Gmyrek", color="Sexo", markers=True, color_discrete_map={"Masculino": "#ff7f0e", "Feminino": "#9467bd"})
        fig4.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig4, use_container_width=True)

    st.write("")

    # -------------------------------------------------------------------------
    # GRÁFICO 5: COMPOSIÇÃO DE GÊNERO (BARRAS AGRUPADAS)
    # -------------------------------------------------------------------------
    st.markdown("#### 📊 Composição de Gênero por Faixas de Impacto (AIOE)")
    
    df_comp = pd.DataFrame([
        {"Faixa": "Baixo Impacto", "Sexo": "Masculino", "Percentual": 65},
        {"Faixa": "Baixo Impacto", "Sexo": "Feminino", "Percentual": 35},
        {"Faixa": "Médio Impacto", "Sexo": "Masculino", "Percentual": 45},
        {"Faixa": "Médio Impacto", "Sexo": "Feminino", "Percentual": 55},
        {"Faixa": "Alto Impacto", "Sexo": "Masculino", "Percentual": 40},
        {"Faixa": "Alto Impacto", "Sexo": "Feminino", "Percentual": 60},
    ])
    
    fig_comp = px.bar(df_comp, x="Faixa", y="Percentual", color="Sexo", barmode="group", text_auto=".1f", color_discrete_map={"Masculino": "#1f77b4", "Feminino": "#e377c2"})
    fig_comp.update_layout(height=400, yaxis_range=[0, 100], margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_comp, use_container_width=True)
