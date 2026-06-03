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

    st.info("""
    Este simulador utiliza os indicadores de exposição à Inteligência Artificial calculados ao longo deste estudo a partir da metodologia AIOE (Felten et al.) e das classificações propostas pela Organização Internacional do Trabalho (Gmyrek et al., 2025).
    
    O objetivo não é prever substituição de empregos individuais, mas estimar o grau de exposição potencial das tarefas associadas a cada ocupação diante do avanço das tecnologias de IA generativa.
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

    st.info(f"""
    A ocupação selecionada apresentou um score AIOE de {score_real_ia:.2f}.
    
    Esse indicador representa o potencial de exposição das atividades desempenhadas nessa profissão às capacidades atuais da Inteligência Artificial, especialmente em tarefas relacionadas ao processamento de informação, geração de conteúdo, análise documental e tomada de decisão baseada em conhecimento.
    """)

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

    st.success("""
    Interpretação do indicador:
    
    🟢 Baixa exposição: predominância de atividades manuais, operacionais ou dependentes de interação física.
    
    🟡 Exposição intermediária: coexistência de tarefas suscetíveis à automação e atividades que exigem julgamento humano.
    
    🔴 Alta exposição: forte presença de tarefas cognitivas, administrativas ou informacionais que podem ser complementadas ou parcialmente automatizadas por sistemas de IA.
    """)

    # Card dinâmico da OIT/ILO
    st.markdown(f"### 📑 Diagnóstico OIT (Métrica Gmyrek): **{classificacao_oit}**")
    if cor_card == "blue":
        st.info(detalhe_oit)
    elif cor_card == "red":
        st.error(detalhe_oit)
    else:
        st.success(detalhe_oit)

    st.info("""
    A classificação da OIT distingue dois fenômenos diferentes:
    
    • Augmentation (Aumento): quando a IA tende a complementar o trabalho humano, elevando produtividade e eficiência.
    
    • Automation (Automação): quando parte significativa das tarefas pode ser executada diretamente por sistemas automatizados.
    
    Assim, alta exposição não significa necessariamente eliminação da ocupação, mas transformação das atividades desempenhadas.
    """)

    st.divider()
    
    # ==========================================
    # MERCADO REAL (PNAD CONTÍNUA COORTE)
    # ==========================================

    st.divider()

    st.subheader("📚 Interpretação Acadêmica")
    
    st.markdown(f"""
    Considerando os parâmetros selecionados, a ocupação **{ocupacao_selecionada}** apresenta um indicador de exposição de **{score_real_ia:.2f}**.
    
    Segundo os referenciais adotados neste estudo, ocupações com níveis mais elevados de exposição tendem a sofrer transformações mais rápidas decorrentes da adoção de ferramentas de Inteligência Artificial, especialmente em atividades relacionadas ao processamento de informação e apoio à tomada de decisão.
    
    O impacto efetivo, entretanto, depende de fatores complementares como escolaridade, qualificação profissional, contexto econômico, setor de atuação e velocidade de adoção tecnológica.
    """)
    
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

    st.divider()

       st.divider()

    # ==========================================
    # COMPARAÇÃO COM A MÉDIA NACIONAL
    # ==========================================

    st.subheader("📈 Comparação com a Média Nacional")

    media_nacional = float(df["AIOE_SCORE"].mean())

    fig_comp = go.Figure()

    fig_comp.add_trace(
        go.Bar(
            x=["Média Nacional", ocupacao_selecionada],
            y=[media_nacional, score_real_ia],
            text=[
                f"{media_nacional:.2f}",
                f"{score_real_ia:.2f}"
            ],
            textposition="outside"
        )
    )

    fig_comp.update_layout(
        title="Comparação do Score AIOE",
        yaxis_title="Score AIOE",
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig_comp,
        use_container_width=True
    )

    diferenca = score_real_ia - media_nacional

    if diferenca > 0:
        st.info(f"""
        A ocupação selecionada apresenta exposição à IA superior à média nacional.

        Diferença observada: **+{diferenca:.2f} pontos** em relação ao conjunto das ocupações analisadas.

        Isso sugere que as atividades associadas a essa profissão possuem maior proximidade com tarefas potencialmente impactadas por ferramentas de Inteligência Artificial.
        """)
    else:
        st.info(f"""
        A ocupação selecionada apresenta exposição à IA inferior à média nacional.

        Diferença observada: **{diferenca:.2f} pontos** em relação à média das ocupações analisadas.

        Isso indica que as atividades exercidas nessa profissão tendem a depender mais de habilidades manuais, operacionais ou de interação humana direta.
        """)

    st.divider()

    st.success("""
    Conclusão da Simulação

    Os resultados apresentados devem ser interpretados como indicadores de exposição ocupacional e não como previsões determinísticas de substituição de empregos.

    A literatura recente aponta que os efeitos da Inteligência Artificial tendem a ocorrer principalmente por transformação das tarefas, reorganização dos processos produtivos e aumento de produtividade, podendo gerar tanto riscos quanto oportunidades para trabalhadores e organizações.

    Dessa forma, ocupações com maior exposição não necessariamente desaparecerão, mas tendem a sofrer mudanças mais intensas em seus processos de trabalho ao longo dos próximos anos.
    """)
