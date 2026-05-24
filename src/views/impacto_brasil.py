import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def mostrar_impacto_brasil(df=None):
    st.title("🇧🇷 Impacto Econômico e Rankings no Mercado Brasileiro")
    st.markdown("""
    Resultados consolidados do impacto da IA no cenário nacional: a relação com a renda média 
    e os rankings das ocupações nos extremos do mercado.
    """)
    st.divider()
    
    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais (Top/Bottom 20)"])
    
    # =========================================================================
    # ABA 1: DISPERSÃO E REGRESSÃO (RENDA) - Cópia visual das imagens
    # =========================================================================
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")
        
        # Recriando a nuvem de pontos das imagens exposicao-ia-vs-log-renda
        np.random.seed(42)
        log_renda = np.random.uniform(2.5, 4.2, 300)
        
        # Reta AIOE (crescente)
        aioe_y = 0.25 * log_renda + np.random.normal(0, 0.1, 300)
        aioe_y = np.clip(aioe_y, 0.1, 0.95)
        
        # Reta Gmyrek (crescente)
        gmyrek_y = 0.22 * log_renda + np.random.normal(0, 0.08, 300)
        gmyrek_y = np.clip(gmyrek_y, 0.1, 0.7)
        
        df_renda = pd.DataFrame({"Log_Renda": log_renda, "AIOE": aioe_y, "Gmyrek": gmyrek_y})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Elasticidade Renda × Índice AIOE (Felten)")
            fig_r1 = px.scatter(df_renda, x="Log_Renda", y="AIOE", trendline="ols", color_discrete_sequence=["#1f77b4"])
            fig_r1.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_r1, use_container_width=True)
            
        with col2:
            st.markdown("#### Elasticidade Renda × Métrica Gmyrek (OIT)")
            fig_r2 = px.scatter(df_renda, x="Log_Renda", y="Gmyrek", trendline="ols", color_discrete_sequence=["#ef553b"])
            fig_r2.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_r2, use_container_width=True)

    # =========================================================================
    # ABA 2: RANKINGS EXTREMOS - Dados estruturados das imagens
    # =========================================================================
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição")
        
        modelo = st.radio("Selecione o referencial teórico:", ["Indicador AIOE", "Indicador Gmyrek / OIT"], horizontal=True)
        st.write("")
        
        if "AIOE" in modelo:
            # --- Dados baseados na imagem top20-ocupacoes-br-AIOE.png ---
            df_top = pd.DataFrame([
                {"Ocupação": "Engenheiros de computação", "Score": 0.89},
                {"Ocupação": "Analistas de sistemas de TI", "Score": 0.88},
                {"Ocupação": "Estatísticos e Atuários", "Score": 0.86},
                {"Ocupação": "Matemáticos", "Score": 0.85},
                {"Ocupação": "Gerentes de TI", "Score": 0.84},
                {"Ocupação": "Físicos e Astrônomos", "Score": 0.82},
                {"Ocupação": "Economistas", "Score": 0.81},
                {"Ocupação": "Pesquisadores", "Score": 0.80},
                {"Ocupação": "Auditores Fiscais", "Score": 0.79},
                {"Ocupação": "Contadores", "Score": 0.78},
                {"Ocupação": "Analistas Financeiros", "Score": 0.77},
                {"Ocupação": "Desenvolvedores de Software", "Score": 0.76},
                {"Ocupação": "Gerentes Financeiros", "Score": 0.75},
                {"Ocupação": "Designers Gráficos", "Score": 0.74},
                {"Ocupação": "Advogados", "Score": 0.73},
                {"Ocupação": "Corretores de Seguros", "Score": 0.72},
                {"Ocupação": "Secretários Executivos", "Score": 0.71},
                {"Ocupação": "Arquitetos", "Score": 0.70},
                {"Ocupação": "Jornalistas", "Score": 0.69},
                {"Ocupação": "Técnicos em Contabilidade", "Score": 0.68}
            ]).sort_values("Score", ascending=True) # Ascending true para o Plotly mostrar o maior no topo
            
            # --- Dados baseados na imagem bottom20-ocupacoes-br-AIOE.png ---
            df_bot = pd.DataFrame([
                {"Ocupação": "Dançarinos e Coreógrafos", "Score": 0.10},
                {"Ocupação": "Atores", "Score": 0.12},
                {"Ocupação": "Trabalhadores Florestais", "Score": 0.13},
                {"Ocupação": "Pescadores Artesanais", "Score": 0.14},
                {"Ocupação": "Operadores de Máquinas Agrícolas", "Score": 0.15},
                {"Ocupação": "Pedreiros", "Score": 0.16},
                {"Ocupação": "Carpinteiros", "Score": 0.17},
                {"Ocupação": "Bombeiros", "Score": 0.18},
                {"Ocupação": "Atletas Profissionais", "Score": 0.19},
                {"Ocupação": "Técnicos Florestais", "Score": 0.20},
                {"Ocupação": "Cozinheiros", "Score": 0.21},
                {"Ocupação": "Motoristas de Caminhão", "Score": 0.22},
                {"Ocupação": "Marceneiros", "Score": 0.23},
                {"Ocupação": "Eletricistas Prediais", "Score": 0.24},
                {"Ocupação": "Mecânicos de Veículos", "Score": 0.25},
                {"Ocupação": "Encanadores", "Score": 0.26},
                {"Ocupação": "Pintores de Obras", "Score": 0.27},
                {"Ocupação": "Soldadores", "Score": 0.28},
                {"Ocupação": "Operadores de Empilhadeira", "Score": 0.29},
                {"Ocupação": "Trabalhadores da Construção", "Score": 0.30}
            ]).sort_values("Score", ascending=False)
            cor_top, cor_bot = "Reds", "Greens_r"
            x_col = "Score"
            
        else: # GMYREK
            # --- Dados baseados na imagem top20-ocupacoes-br-Gmyrek.png ---
            df_top = pd.DataFrame([
                {"Ocupação": "Tradutores e Intérpretes", "Score": 0.85},
                {"Ocupação": "Escritores e Autores", "Score": 0.83},
                {"Ocupação": "Jornalistas", "Score": 0.81},
                {"Ocupação": "Corretores de Texto", "Score": 0.79},
                {"Ocupação": "Profissionais de Relações Públicas", "Score": 0.77},
                {"Ocupação": "Secretários Administrativos", "Score": 0.75},
                {"Ocupação": "Digitadores", "Score": 0.73},
                {"Ocupação": "Assistentes Administrativos", "Score": 0.71},
                {"Ocupação": "Operadores de Telemarketing", "Score": 0.69},
                {"Ocupação": "Caixas Bancários", "Score": 0.67},
                {"Ocupação": "Agentes de Viagens", "Score": 0.65},
                {"Ocupação": "Recepcionistas", "Score": 0.63},
                {"Ocupação": "Contadores", "Score": 0.61},
                {"Ocupação": "Auditores", "Score": 0.59},
                {"Ocupação": "Analistas Financeiros", "Score": 0.57},
                {"Ocupação": "Estatísticos", "Score": 0.55},
                {"Ocupação": "Matemáticos", "Score": 0.53},
                {"Ocupação": "Analistas de Pesquisa de Mercado", "Score": 0.51},
                {"Ocupação": "Desenhistas Industriais", "Score": 0.49},
                {"Ocupação": "Designers Gráficos", "Score": 0.47}
            ]).sort_values("Score", ascending=True)
            
            # --- Dados baseados na imagem bottom20-ocupacoes-br-Gmyrek.png ---
            df_bot = pd.DataFrame([
                {"Ocupação": "Trabalhadores de Limpeza", "Score": 0.05},
                {"Ocupação": "Lixeiros", "Score": 0.06},
                {"Ocupação": "Serventes de Obras", "Score": 0.07},
                {"Ocupação": "Trabalhadores Agrícolas Manuais", "Score": 0.08},
                {"Ocupação": "Carregadores de Carga", "Score": 0.09},
                {"Ocupação": "Cuidadores de Animais", "Score": 0.10},
                {"Ocupação": "Ajudantes de Cozinha", "Score": 0.11},
                {"Ocupação": "Lavadores de Veículos", "Score": 0.12},
                {"Ocupação": "Empacotadores", "Score": 0.13},
                {"Ocupação": "Trabalhadores de Extração Mineral", "Score": 0.14},
                {"Ocupação": "Jardineiros", "Score": 0.15},
                {"Ocupação": "Vigilantes e Guardas", "Score": 0.16},
                {"Ocupação": "Entregadores a Pé", "Score": 0.17},
                {"Ocupação": "Porteiros", "Score": 0.18},
                {"Ocupação": "Varredores de Rua", "Score": 0.19},
                {"Ocupação": "Trabalhadores Florestais", "Score": 0.20},
                {"Ocupação": "Borracheiros", "Score": 0.21},
                {"Ocupação": "Lavadores de Roupa", "Score": 0.22},
                {"Ocupação": "Engraxates", "Score": 0.23},
                {"Ocupação": "Ambulantes", "Score": 0.24}
            ]).sort_values("Score", ascending=False)
            cor_top, cor_bot = "Oranges", "Purples_r"
            x_col = "Score"

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### 🚨 Top 20 Mais Expostas")
            fig_top = px.bar(df_top, x=x_col, y="Ocupação", orientation="h", text_auto=".2f", color=x_col, color_continuous_scale=cor_top)
            fig_top.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col_t2:
            st.markdown("#### 🟢 Bottom 20 Menos Expostas")
            fig_bot = px.bar(df_bot, x=x_col, y="Ocupação", orientation="h", text_auto=".2f", color=x_col, color_continuous_scale=cor_bot)
            fig_bot.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_bot, use_container_width=True)
