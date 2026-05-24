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
            try:
                st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-AIOE.png"), use_container_width=True)
            except:
                st.warning("Imagem não encontrada no diretório img/")
        with col2:
            st.markdown("#### Elasticidade Renda × Métrica Gmyrek (OIT)")
            try:
                st.image(os.path.join(img_dir, "exposicao-ia-vs-log-renda-Gmyrek.png"), use_container_width=True)
            except:
                st.warning("Imagem não encontrada no diretório img/")

    # =========================================================================
    # ABA 2: RANKINGS EXTREMOS (GRÁFICOS INTERATIVOS PLOTLY COM DADOS REAIS)
    # =========================================================================
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição")
        modelo = st.radio("Selecione o referencial teórico:", ["Indicador AIOE (Felten et al.)", "Indicador Gmyrek / OIT"], horizontal=True)
        st.write("")
        
        col_t1, col_t2 = st.columns(2)
        
        if "AIOE" in modelo:
            # --- DADOS EXTRAÍDOS DA IMAGEM: top20-ocupacoes-br-AIOE.png ---
            df_top = pd.DataFrame([
                {"Ocupação": "Especialistas em métodos pedag...", "Score": 0.69},
                {"Ocupação": "Agentes de saúde pública e de d...", "Score": 0.68},
                {"Ocupação": "Técnicos e controladores do tráf...", "Score": 0.67},
                {"Ocupação": "Engenheiros eletricistas e eletrô...", "Score": 0.67},
                {"Ocupação": "Profissionais em pesquisa e aná...", "Score": 0.66},
                {"Ocupação": "Profissionais do jornalismo", "Score": 0.66},
                {"Ocupação": "Despachantes aduaneiros", "Score": 0.66},
                {"Ocupação": "Professores do ensino profission...", "Score": 0.65},
                {"Ocupação": "Professores do ensino médio", "Score": 0.65},
                {"Ocupação": "Engenheiros de telecomunicaçõ...", "Score": 0.65},
                {"Ocupação": "Engenheiros civis", "Score": 0.65},
                {"Ocupação": "Delegados de polícia", "Score": 0.65},
                {"Ocupação": "Professores universitários e do ...", "Score": 0.64},
                {"Ocupação": "Professores do ensino fundame...", "Score": 0.64},
                {"Ocupação": "Operadores de instalações de tr...", "Score": 0.64},
                {"Ocupação": "Físicos e astrônomos", "Score": 0.64},
                {"Ocupação": "Engenheiros químicos e afins", "Score": 0.64},
                {"Ocupação": "Engenheiros mecânicos", "Score": 0.64},
                {"Ocupação": "Designers de moda", "Score": 0.64},
                {"Ocupação": "Administradores", "Score": 0.64}
            ])
            
            # --- DADOS EXTRAÍDOS DA IMAGEM: 20-ocupacoes-br-AIOE.png (Bottom 20) ---
            df_bot = pd.DataFrame([
                {"Ocupação": "Trabalhadores da pintura de eq...", "Score": 0.28},
                {"Ocupação": "Lavadores de vidros e afins", "Score": 0.28},
                {"Ocupação": "Atendentes de enfermagem, pa...", "Score": 0.29},
                {"Ocupação": "Prepraradores e operadores d...", "Score": 0.30},
                {"Ocupação": "Varredores e afins", "Score": 0.31},
                {"Ocupação": "Trabalhadores dos serviços fu...", "Score": 0.31},
                {"Ocupação": "Operadores de usinagem con...", "Score": 0.31},
                {"Ocupação": "Empregados que prestam ser...", "Score": 0.31},
                {"Ocupação": "Ceramistas (preparação e fab...", "Score": 0.31},
                {"Ocupação": "Vendedores em quiosques e b...", "Score": 0.32},
                {"Ocupação": "Trabalhadores florestais", "Score": 0.32},
                {"Ocupação": "Pescadores e trabalhadores ...", "Score": 0.32},
                {"Ocupação": "Operadores de equipamentos ...", "Score": 0.32},
                {"Ocupação": "Limpadores de edifícios e afins", "Score": 0.32},
                {"Ocupação": "Condutores de veículos de tra...", "Score": 0.32},
                {"Ocupação": "Trabalhadores de serviços do...", "Score": 0.33},
                {"Ocupação": "Trabalhadores da agricultura ...", "Score": 0.33},
                {"Ocupação": "Profissionais das terapias alt...", "Score": 0.33},
                {"Ocupação": "Ocupações de apoio as ati...", "Score": 0.33},
                {"Ocupação": "Cobradores de transportes t...", "Score": 0.33}
            ])
            
            escala_top = "Reds"
            escala_bot = "Blues_r" # Conforme o azul da imagem base AIOE

        else:
            # --- DADOS EXTRAÍDOS DA IMAGEM: top20-ocupacoes-br-Gmyrek.png ---
            df_top = pd.DataFrame([
                {"Ocupação": "Tradutores, intérpretes e linguistas", "Score": 0.56},
                {"Ocupação": "Profissionais de Relações Públicas", "Score": 0.53},
                {"Ocupação": "Produtores de rádio, televisão e...", "Score": 0.53},
                {"Ocupação": "Jornalistas", "Score": 0.53},
                {"Ocupação": "Diretores de cinema, de teatro e a...", "Score": 0.53},
                {"Ocupação": "Autores e escritores", "Score": 0.53},
                {"Ocupação": "Assistentes administrativos e sec...", "Score": 0.52},
                {"Ocupação": "Técnicos de biblioteca", "Score": 0.52},
                {"Ocupação": "Recepcionistas de escritórios", "Score": 0.52},
                {"Ocupação": "Operadores de equipamento pro...", "Score": 0.52},
                {"Ocupação": "Auxiliares e ajudantes de escritór...", "Score": 0.52},
                {"Ocupação": "Arquivistas de escritório", "Score": 0.52},
                {"Ocupação": "Agentes de organização e de mé...", "Score": 0.52},
                {"Ocupação": "Agentes de administração da em...", "Score": 0.52},
                {"Ocupação": "Agentes de contabilidade e cont...", "Score": 0.52},
                {"Ocupação": "Profissionais da organização da a...", "Score": 0.51},
                {"Ocupação": "Profissionais de publicidade e m...", "Score": 0.51},
                {"Ocupação": "Bibliotecários, documentaristas ...", "Score": 0.51},
                {"Ocupação": "Analistas de sistemas", "Score": 0.51},
                {"Ocupação": "Administradores", "Score": 0.51}
            ])
            
            # --- DADOS EXTRAÍDOS DA IMAGEM: 20-ocupacoes-br-Gmyrek.png (Bottom 20) ---
            df_bot = pd.DataFrame([
                {"Ocupação": "Diretores gerais e gerentes gerais...", "Score": 0.05},
                {"Ocupação": "Soldadores e oxicortadores", "Score": 0.07},
                {"Ocupação": "Serventes de obras", "Score": 0.07},
                {"Ocupação": "Preparadores e montadores de e...", "Score": 0.07},
                {"Ocupação": "Pedreiros", "Score": 0.07},
                {"Ocupação": "Operadores de usinagem conve...", "Score": 0.07},
                {"Ocupação": "Operadores de instalação de pro...", "Score": 0.07},
                {"Ocupação": "Operadores de instalação de co...", "Score": 0.07},
                {"Ocupação": "Modeladores de matrizes", "Score": 0.07},
                {"Ocupação": "Modeladores de madeira", "Score": 0.07},
                {"Ocupação": "Mecânicos", "Score": 0.07},
                {"Ocupação": "Marceneiros", "Score": 0.07},
                {"Ocupação": "Ferramenteiros e afins", "Score": 0.07},
                {"Ocupação": "Ceramistas (preparação e fabric...", "Score": 0.07},
                {"Ocupação": "Carpinteiros", "Score": 0.07},
                {"Ocupação": "Borracheiros e afins", "Score": 0.07},
                {"Ocupação": "Trabalhadores de forjamento d...", "Score": 0.08},
                {"Ocupação": "Técnicos de laboratório e raios-X", "Score": 0.08},
                {"Ocupação": "Pintores de veículos e afins", "Score": 0.08},
                {"Ocupação": "Pescadores e trabalhadores de...", "Score": 0.08}
            ])
            
            escala_top = "Oranges"
            escala_bot = "Purples_r" # Conforme a cor da imagem Gmyrek base

        # --- RENDERIZAÇÃO INTERATIVA PLOTLY ---
        with col_t1:
            st.markdown("#### 🚨 Top 20 Ocupações Mais Expostas")
            # Ordenando do menor para o maior para o Plotly colocar o maior no topo do eixo Y
            df_top = df_top.sort_values(by="Score", ascending=True)
            
            fig_top = px.bar(
                df_top, x="Score", y="Ocupação", orientation="h", 
                text_auto=".2f", color="Score", color_continuous_scale=escala_top
            )
            fig_top.update_layout(
                height=650, showlegend=False, 
                margin=dict(l=10, r=20, t=10, b=10),
                yaxis_title=None, xaxis_title="Score"
            )
            st.plotly_chart(fig_top, use_container_width=True)
            
        with col_t2:
            st.markdown("#### 🟢 Bottom 20 Ocupações Menos Expostas")
            # Ordenando do maior para o menor para manter a consistência de quem está mais na base
            df_bot = df_bot.sort_values(by="Score", ascending=False)
            
            fig_bot = px.bar(
                df_bot, x="Score", y="Ocupação", orientation="h", 
                text_auto=".2f", color="Score", color_continuous_scale=escala_bot
            )
            fig_bot.update_layout(
                height=650, showlegend=False, 
                margin=dict(l=10, r=20, t=10, b=10),
                yaxis_title=None, xaxis_title="Score"
            )
            st.plotly_chart(fig_bot, use_container_width=True)
