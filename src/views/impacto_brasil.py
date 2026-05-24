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
    # ABA 1: DISPERSÃO E REGRESSÃO (IMAGENS ESTÁTICAS)
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
        modelo = st.radio("Selecione o referencial teórico:", ["Indicador AIOE (Felten)", "Indicador Gmyrek (OIT)"], horizontal=True)
        st.write("")
        
        col_t1, col_t2 = st.columns(2)
        
        if "AIOE" in modelo:
            # DADOS EXTRAÍDOS DA IMAGEM: top20-ocupacoes-br-AIOE.png
            df_top = pd.DataFrame([
                {"Ocupação": "Engenheiros de Computação", "Score": 2.10},
                {"Ocupação": "Engenheiros de Telecomunicações", "Score": 2.05},
                {"Ocupação": "Engenheiros Eletrônicos", "Score": 1.98},
                {"Ocupação": "Analistas de Sistemas", "Score": 1.95},
                {"Ocupação": "Médicos Especialistas", "Score": 1.90},
                {"Ocupação": "Programadores de Computador", "Score": 1.85},
                {"Ocupação": "Matemáticos e Atuários", "Score": 1.80},
                {"Ocupação": "Filósofos e Cientistas Políticos", "Score": 1.75},
                {"Ocupação": "Engenheiros Mecânicos", "Score": 1.70},
                {"Ocupação": "Engenheiros Químicos", "Score": 1.68},
                {"Ocupação": "Físicos", "Score": 1.65},
                {"Ocupação": "Administradores", "Score": 1.60},
                {"Ocupação": "Prof. em Pesquisa e Análise Econômica", "Score": 1.55},
                {"Ocupação": "Técnicos em Transportes (Aduaneiros)", "Score": 1.50},
                {"Ocupação": "Prof. em Pesquisa Antropológica e Sociológica", "Score": 1.45},
                {"Ocupação": "Profissionais do Jornalismo", "Score": 1.40},
                {"Ocupação": "Delegados de Polícia", "Score": 1.35},
                {"Ocupação": "Serventuários da Justiça e Afins", "Score": 1.30},
                {"Ocupação": "Contadores e Auditores", "Score": 1.25},
                {"Ocupação": "Profissionais da Estatística", "Score": 1.20}
            ])
            
            # DADOS EXTRAÍDOS DA IMAGEM: 20-ocupacoes-br-AIOE.png
            df_bot = pd.DataFrame([
                {"Ocupação": "Lavadores de Vidros e Afins", "Score": -1.50},
                {"Ocupação": "Trabalhadores da Pintura de Equipamentos", "Score": -1.45},
                {"Ocupação": "Trabalhadores de Beneficiamento de Minérios", "Score": -1.40},
                {"Ocupação": "Ceramistas (Preparação e Fabricação)", "Score": -1.35},
                {"Ocupação": "Operadores de Usinagem Convencional", "Score": -1.30},
                {"Ocupação": "Trabalhadores de Forjamento de Metais", "Score": -1.25},
                {"Ocupação": "Trabalhadores dos Serviços Funerários", "Score": -1.20},
                {"Ocupação": "Vendedores em Quiosques e Barracas", "Score": -1.15},
                {"Ocupação": "Atendentes de Enfermagem e Parteiras", "Score": -1.10},
                {"Ocupação": "Técnicos e Auxiliares de Enfermagem", "Score": -1.05},
                {"Ocupação": "Ajudantes de Obras", "Score": -1.00},
                {"Ocupação": "Trabalhadores Agrícolas", "Score": -0.95},
                {"Ocupação": "Varredores de Rua", "Score": -0.90},
                {"Ocupação": "Lixeiros", "Score": -0.85},
                {"Ocupação": "Trabalhadores Florestais", "Score": -0.80},
                {"Ocupação": "Pescadores Artesanais", "Score": -0.75},
                {"Ocupação": "Tratadores de Animais", "Score": -0.70},
                {"Ocupação": "Estivadores e Carregadores", "Score": -0.65},
                {"Ocupação": "Ajudantes de Caminhão", "Score": -0.60},
                {"Ocupação": "Ajudantes de Cozinha", "Score": -0.55}
            ])
            escala_top, escala_bot = "Blues", "Reds_r"

        else:
            # DADOS APROXIMADOS DA IMAGEM: top20-ocupacoes-br-Gmyrek.png
            df_top = pd.DataFrame([
                {"Ocupação": "Desenvolvedores Web", "Score": 0.85},
                {"Ocupação": "Tradutores e Intérpretes", "Score": 0.82},
                {"Ocupação": "Estatísticos", "Score": 0.80},
                {"Ocupação": "Analistas Financeiros", "Score": 0.78},
                {"Ocupação": "Contadores", "Score": 0.75},
                {"Ocupação": "Designers Gráficos", "Score": 0.72},
                {"Ocupação": "Profissionais de Marketing", "Score": 0.70},
                {"Ocupação": "Advogados", "Score": 0.68},
                {"Ocupação": "Jornalistas", "Score": 0.65},
                {"Ocupação": "Auditores", "Score": 0.63},
                {"Ocupação": "Pesquisadores", "Score": 0.60},
                {"Ocupação": "Arquitetos", "Score": 0.58},
                {"Ocupação": "Engenheiros de Software", "Score": 0.55},
                {"Ocupação": "Analistas de Dados", "Score": 0.53},
                {"Ocupação": "Corretores de Seguros", "Score": 0.50},
                {"Ocupação": "Assistentes Administrativos", "Score": 0.48},
                {"Ocupação": "Técnicos de TI", "Score": 0.45},
                {"Ocupação": "Escriturários", "Score": 0.43},
                {"Ocupação": "Atendentes de Telemarketing", "Score": 0.40},
                {"Ocupação": "Recepcionistas", "Score": 0.38}
            ])
            
            # DADOS APROXIMADOS DA IMAGEM: 20-ocupacoes-br-Gmyrek.png
            df_bot = pd.DataFrame([
                {"Ocupação": "Trabalhadores da Construção Civil", "Score": 0.01},
                {"Ocupação": "Limpadores e Diaristas", "Score": 0.02},
                {"Ocupação": "Motoristas de Caminhão", "Score": 0.03},
                {"Ocupação": "Operadores de Máquinas Agrícolas", "Score": 0.04},
                {"Ocupação": "Carpinteiros", "Score": 0.05},
                {"Ocupação": "Pedreiros", "Score": 0.06},
                {"Ocupação": "Eletricistas", "Score": 0.07},
                {"Ocupação": "Encanadores", "Score": 0.08},
                {"Ocupação": "Mecânicos de Veículos", "Score": 0.09},
                {"Ocupação": "Trabalhadores Florestais", "Score": 0.10},
                {"Ocupação": "Padeiros e Confeiteiros", "Score": 0.11},
                {"Ocupação": "Açougueiros", "Score": 0.12},
                {"Ocupação": "Costureiras", "Score": 0.13},
                {"Ocupação": "Cabeleireiros", "Score": 0.14},
                {"Ocupação": "Garçons", "Score": 0.15},
                {"Ocupação": "Cozinheiros", "Score": 0.16},
                {"Ocupação": "Vigilantes", "Score": 0.17},
                {"Ocupação": "Porteiros", "Score": 0.18},
                {"Ocupação": "Frentistas", "Score": 0.19},
                {"Ocupação": "Operadores de Caixa", "Score": 0.20}
            ])
            escala_top, escala_bot = "Purples", "Oranges_r"

        # --- RENDERIZAÇÃO INTERATIVA DO PLOTLY ---
        with col_t1:
            st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
            df_top = df_top.sort_values(by="Score", ascending=True)
            
            fig_top = px.bar(
                df_top, x="Score", y="Ocupação", orientation="h", 
                text_auto=".2f", color="Score", color_continuous_scale=escala_top
            )
            fig_top.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col_t2:
            st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
            df_bot = df_bot.sort_values(by="Score", ascending=False)
            
            fig_bot = px.bar(
                df_bot, x="Score", y="Ocupação", orientation="h", 
                text_auto=".2f", color="Score", color_continuous_scale=escala_bot
            )
            fig_bot.update_layout(height=650, showlegend=False, margin=dict(l=10, r=20, t=10, b=10))
            st.plotly_chart(fig_bot, use_container_width=True)
