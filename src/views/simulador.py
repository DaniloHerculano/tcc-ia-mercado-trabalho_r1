import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def mostrar_simulador(df):
    st.title("🤖 Simulador de Exposição e Impacto da IA")
    st.markdown("""
    Selecione uma ocupação e monte o perfil demográfico para simular o nível de exposição e a 
    classificação de risco de acordo com a metodologia da **Organização Internacional do Trabalho (OIT/Gmyrek et al., 2025)**.
    """)

    st.divider()

    # ==========================================
    # VALIDAR COLUNAS CRÍTICAS
    # ==========================================
    colunas_necessarias = ["TITULO_LIMPO", "AIOE_SCORE", "UF", "Sexo"]
    for col in colunas_necessarias:
        if col not in df.columns:
            st.error(f"Coluna essencial '{col}' não encontrada na base de dados.")
            return

    # ==========================================
    # PAINEL DE ENTRADAS (FILTROS E SELEÇÕES)
    # ==========================================
    st.subheader("👤 Configuração do Perfil Profissional")
    
    # 1. Seleção da Ocupação Real
    lista_ocupacoes = sorted(df["TITULO_LIMPO"].dropna().unique())
    ocupacao_selecionada = st.selectbox("💼 Selecione a Ocupação (CBO):", lista_ocupacoes)
    
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        sexo = st.selectbox("👤 Sexo:", sorted(df["Sexo"].dropna().unique()))
        uf = st.selectbox("🌎 Unidade Federativa (UF):", sorted(df["UF"].dropna().unique()))
        idade = st.slider("🎂 Idade:", 14, 80, 30)

    with col2:
        # Escolaridade é a chave para a classificação da OIT (Gmyrek)
        escolaridade = st.selectbox(
            "🎓 Grau de Escolaridade:",
            [
                "Até Ensino Fundamental Incompleto/Completo",
                "Ensino Médio Completo",
                "Ensino Superior Incompleto/Completo"
            ]
        )
        
        # Recupera as médias reais daquela ocupação na PNAD para sugerir ao usuário
        df_ocup = df[df["TITULO_LIMPO"] == ocupacao_selecionada]
        renda_media_real = float(df_ocup["Rendimento_Mensal"].mean()) if "Rendimento_Mensal" in df_ocup.columns else 2500.0
        if np.isnan(renda_media_real): renda_media_real = 2500.0

        renda = st.number_input(
            "💰 Renda Mensal Simulada (R$):", 
            min_value=0, 
            max_value=100000, 
            value=int(renda_media_real), 
            step=500
        )

    st.divider()

    # ==========================================
    # PROCESSAMENTO DOS SCORES REAIS
    # ==========================================
    # Captura os scores fixados por transfer learning no seu pipeline
    score_real_ia = float(df_ocup["AIOE_SCORE"].iloc[0]) if not df_ocup.empty else 0.0
    
    # Define o nível de impacto bruto baseado nos quartis clássicos (0.45 e 0.75)
    if score_real_ia >= 0.75:
        nivel_impacto = "🔴 Alto"
    elif score_real_ia >= 0.45:
        nivel_impacto = "🟡 Médio"
    else:
        nivel_impacto = "🟢 Baixo"

    # ==========================================
    # REGRA DE CLASSIFICAÇÃO GMYREK ET AL. (2025/ILO)
    # ==========================================
    # Alta exposição + alta escolaridade = Augmentation (Potencial de aumento)
    # Alta exposição + baixa escolaridade = Automation (Risco de automação)
    if score_real_ia >= 0.50:  # Linha de corte mediana/alta exposição
        if escolaridade in ["Ensino Médio Completo", "Ensino Superior Incompleto/Completo"]:
            classificacao_oit = "🚀 Potencial de Aumento (Augmentation)"
            cor_card = "blue"
            detalhe_oit = "A IA tende a complementar as tarefas deste profissional, aumentando sua produtividade e eficiência."
        else:
            classificacao_oit = "⚠️ Risco de Automação (Automation)"
            cor_card = "red"
            detalhe_oit = "A ocupação possui tarefas rotineiras ou administrativas expostas que correm risco de substituição direta."
    else:
        classificacao_oit = "🟢 Baixa / Moderada Exposição"
        cor_card = "green"
        detalhe_oit = "Ocupação predominantemente manual, operacional ou de forte interação humana direta, pouco afetada no momento."

    # ==========================================
    # EXIBIÇÃO DE RESULTADOS (KPIs)
    # ==========================================
    st.subheader("📊 Resultado da Simulação")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("🤖 Score AIOE Real", f"{score_real_ia:.2f}")
    kpi2.metric("⚡ Nível de Exposição", nivel_impacto)
    kpi3.metric("💼 Ocupação Alvo", ocupacao_selecionada)

    # Gráfico de Velocímetro Customizado
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_real_ia,
        title={'text': "Índice de Exposição à Inteligência Artificial (AIOE)"},
        gauge={
            'axis': {'range': [0, 1], 'tickwidth': 1},
            'bar': {'color': "#2b5c8f", 'thickness': 0.25},
            'steps': [
                {'range': [0, 0.45], 'color': "#dcfce7"}, # Verde claro
                {'range': [0.45, 0.75], 'color': "#fef9c3"}, # Amarelo claro
                {'range': [0.75, 1], 'color': "#fee2e2"} # Vermelho claro
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score_real_ia
            }
        }
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Card dinâmico da OIT/ILO
    st.markdown(f"### 📑 Diagnóstico OIT (Métrica Gmyrek): **{classificacao_oit}**")
    if cor_card == "blue":
        st.info(detalhe_oit)
    elif cor_card == "red":
        st.error(detalhe_oit)
    else:
        st.success(detalhe_oit)

    st.divider()

    # ==========================================
    # MERCADO REAL (PNAD CONTÍNUA COORTE)
    # ==========================================
    st.subheader("👥 Contexto Real no Mercado de Trabalho Brasileiro")
    st.markdown("Comparativo do perfil simulado com os trabalhadores reais encontrados na coorte histórica da **PNAD Contínua**:")

    # Filtragem inteligente por proximidade demográfica (UF, Sexo, Idade)
    df_contexto = df[
        (df["TITULO_LIMPO"] == ocupacao_selecionada) & 
        (df["UF"] == uf) & 
        (df["Sexo"] == sexo)
    ]

    if not df_contexto.empty:
        renda_coorte = df_contexto["Rendimento_Mensal"].mean()
        total_trabalhadores = len(df_contexto)
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric(
                label=f"💰 Renda Média Real desta Ocupação em {uf} ({sexo})", 
                value=f"R$ {renda_coorte:,.2f}",
                delta=f"Sua simulação: R$ {renda:,.2f}" if renda != int(renda_coorte) else None
            )
        with c2:
            st.metric(
                label="👥 Amostra de Trabalhadores Identificados no Perfil", 
                value=f"{total_trabalhadores:,} registros"
            )
            
        # Tabela com as principais variações da mesma família ocupacional na base para enriquecer o TCC
        st.write("")
        st.markdown("**Outras variações e subgrupos mapeados para essa mesma área:**")
        
        colunas_exibicao = ["CBO_JOIN", "TITULO_LIMPO", "UF", "Sexo", "Rendimento_Mensal", "AIOE_SCORE"]
        colunas_validas = [c for c in colunas_exibicao if c in df.columns]
        
        st.dataframe(
            df[(df["TITULO_LIMPO"] == ocupacao_selecionada)][colunas_validas].drop_duplicates(subset=["CBO_JOIN"]).head(5),
            use_container_width=True
        )
    else:
        st.warning("⚠️ Não foram encontrados registros com a combinação exata de UF e Sexo para esta profissão na amostragem da PNAD. Exibindo dados consolidados nacionais:")
        st.dataframe(df_ocup[["TITULO_LIMPO", "AIOE_SCORE"]].head(1), use_container_width=True)
