import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_crosswalk(df):
    st.title("🔗 Metodologia e Crosswalk Ocupacional")
    st.markdown("""
    Nesta seção, apresentamos os resultados do processo de compatibilização (*crosswalk*) entre as classificações ocupacionais 
    brasileiras e internacionais, além das taxas de cobertura obtidas para os índices de Inteligência Artificial.
    """)
    
    st.divider()

    # ==========================================
    # 1º GRÁFICO: Cobertura por Etapa
    # ==========================================
    st.subheader("1. Cobertura por Etapa do Crosswalk")
    
    dados_etapas = pd.DataFrame([
        {"Etapa": "CBO → ISCO-88", "Cobertura": 100.0},
        {"Etapa": "ISCO-88 → ISCO-08", "Cobertura": 100.0},
        {"Etapa": "ISCO-08 → SOC", "Cobertura": 100.0},
        {"Etapa": "SOC → Felten/AIOE", "Cobertura": 78.2},
        {"Etapa": "ISCO-08 → Gmyrek Exposure", "Cobertura": 76.8},
        {"Etapa": "ISCO-08 → Gmyrek Mean", "Cobertura": 76.8},
        {"Etapa": "ISCO-08 → Gmyrek SD", "Cobertura": 76.8},
        {"Etapa": "CBO → COD", "Cobertura": 98.7},
    ])

    # Criando o gráfico mantendo exatamente a ordem declarada de cima para baixo
    fig1 = px.bar(
        dados_etapas,
        x="Cobertura",
        y="Etapa",
        orientation="h",
        text="Cobertura",
        color_discrete_sequence=["#1f77b4"] # Azul padrão limpo
    )

    fig1.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig1.update_layout(
        xaxis_title="Cobertura (%)",
        yaxis_title="",
        xaxis_range=[0, 110], # Estendido até 110 para o texto "100.0%" não cortar ou estourar a tela
        yaxis={'categoryorder': 'array', 'categoryarray': dados_etapas['Etapa'].values[::-1]}, # Força a ordem visual correta
        height=450,
        margin=dict(l=20, r=60, t=20, b=20), # Margem da direita (r=60) impede o estouro horizontal
        showlegend=False
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "**Imagem 01:** gráfico da porcentagem de códigos ocupacionais transformados por etapa. *Fonte: Autores do TCC.*"
    )

    st.divider()

    # ==========================================
    # 2º GRÁFICO: Métodos de Compatibilização CBO → COD
    # ==========================================
    st.subheader("2. Distribuição dos Métodos de Compatibilização CBO → COD")
    
    dados_metodos = pd.DataFrame([
        {"Metodo": "match_4d_grupo_base", "Percentual": 78.6},
        {"Metodo": "match_3d_subgrupo", "Percentual": 16.3},
        {"Metodo": "match_1d_grande_grupo", "Percentual": 3.4},
        {"Metodo": "sem_match", "Percentual": 1.3},
        {"Metodo": "match_2d_subgrupo_principal", "Percentual": 0.3}
    ])

    fig2 = px.bar(
        dados_metodos,
        x="Percentual",
        y="Metodo",
        orientation="h",
        text="Percentual",
        color_discrete_sequence=["#1f77b4"]
    )

    fig2.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig2.update_layout(
        xaxis_title="Percentual (%)",
        yaxis_title="",
        xaxis_range=[0, 90], # Ajustado para dar espaço ao texto do maior bloco (78.6%)
        yaxis={'categoryorder': 'array', 'categoryarray': dados_metodos['Metodo'].values[::-1]},
        height=350,
        margin=dict(l=20, r=60, t=20, b=20),
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "**Imagem 02:** gráfico da porcentagem da compatibilização entre a CBO e a COD. *Fonte: Autores do TCC.*"
    )

    st.divider()

    # ==========================================
    # 3º GRÁFICO: Cobertura Final dos Indicadores de IA
    # ==========================================
    st.subheader("3. Cobertura Final dos Indicadores de IA")
    
    dados_cobertura_final = pd.DataFrame([
        {"Indicador": "Crosswalk internacional completo até SOC", "Percentual": 100.0},
        {"Indicador": "Com Felten/AIOE", "Percentual": 78.2},
        {"Indicador": "Com Gmyrek", "Percentual": 76.8},
        {"Indicador": "Com COD para PNAD", "Percentual": 98.7},
        {"Indicador": "Com Felten ou Gmyrek", "Percentual": 92.3},
        {"Indicador": "Com Felten e Gmyrek", "Percentual": 62.6}
    ])

    fig3 = px.bar(
        dados_cobertura_final,
        x="Percentual",
        y="Indicador",
        orientation="h",
        text="Percentual",
        color_discrete_sequence=["#1f77b4"]
    )

    fig3.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig3.update_layout(
        xaxis_title="Percentual (%)",
        yaxis_title="",
        xaxis_range=[0, 110],
        yaxis={'categoryorder': 'array', 'categoryarray': dados_cobertura_final['Indicador'].values[::-1]},
        height=400,
        margin=dict(l=20, r=60, t=20, b=20),
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "**Imagem 10:** gráfico do percentual de cobertura dos indicadores em todo o conjunto de dados do trabalho. *Fonte: Autores do TCC.*"
    )
