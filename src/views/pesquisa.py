import streamlit as st
import pandas as pd

def mostrar_pesquisa(df):
    st.title("🔎 Consulta Detalhada de Ocupações (CBO)")
    st.markdown("""
    Explore o portfólio completo de uma profissão: descrição oficial do Ministério do Trabalho, 
    método de alinhamento estatístico (*crosswalk*) e indicadores demográficos consolidados.
    """)

    st.divider()

    # ======================================
    # VALIDAR COLUNAS MÍNIMAS
    # ======================================
    if "TITULO_LIMPO" not in df.columns:
        st.error("Coluna TITULO_LIMPO não encontrada na base de dados.")
        return

    # ======================================
    # SISTEMA DE BUSCA OTIMIZADO
    # ======================================
    pesquisa = df.copy()
    ocupacoes_disponiveis = sorted(pesquisa["TITULO_LIMPO"].dropna().unique())
    
    busca = st.text_input("⌨️ Digite palavras-chave para filtrar a busca (ex: Gerente, Engenheiro):")
    
    if busca:
        ocupacoes_filtradas = [o for o in ocupacoes_disponiveis if busca.lower() in o.lower()]
    else:
        ocupacoes_filtradas = ocupacoes_disponiveis

    if not ocupacoes_filtradas:
        st.warning("Nenhuma ocupação corresponde aos termos digitados.")
        return

    ocupacao_alvo = st.selectbox("💼 Selecione a Ocupação Desejada:", ocupacoes_filtradas)

    st.divider()

    # Filtra os dados da linha específica
    dados_ocupacao = pesquisa[pesquisa["TITULO_LIMPO"] == ocupacao_alvo]
    linha_registro = dados_ocupacao.iloc[0]

    # ======================================
    # BLOCO 1: IDENTIDADE E METODOLOGIA DO TCC
    # ======================================
    st.subheader("🧠 Rastreabilidade Metodológica")
    st.markdown("Veja como essa ocupação foi processada e integrada no pipeline de dados do projeto:")

    # Criação de cards informativos sobre o backend do algoritmo
    c1, c2, c3 = st.columns(3)
    
    # Identifica o método usado (grupo base, subgrupo, fuzzy, embedding)
    metodo_match = linha_registro.get("AIOE_MATCH_TITLE", "Não informado")
    if pd.isna(metodo_match): metodo_match = "Combinação Estrutural Direta"
    
    c1.metric("🤖 Código CBO Identificado", linha_registro.get("CBO_JOIN", "N/A"))
    c2.metric("🧬 Método de Harmonização", str(metodo_match).replace("match_", ""))
    
    # Se houver score de confiança de embedding residual
    confidence = linha_registro.get("CONFIDENCE_SCORE", None)
    if pd.notna(confidence) and isinstance(confidence, (int, float)):
        c3.metric("🎯 Confiança Semântica (Cosine)", f"{confidence:.2f}")
    else:
        c3.metric("🎯 Alinhamento de Dicionário", "100% Estrutural")

    # Exibe a ementa real extraída por PDFPlumber/OCR
    st.write("")
    with st.expander("📖 Visualizar Descrição Sumária Oficial (MTE)", expanded=True):
        descricao = linha_registro.get("DESCRIÇÃO SUMÁRIA", "Descrição textual não indexada na amostragem residual.")
        if pd.isna(descricao): descricao = "Texto sumário indisponível para esta família ocupacional."
        st.write(descricao)

    st.divider()

    # ======================================
    # BLOCO 2: MÉTRICAS HISTÓRICAS DE EXPOSIÇÃO À IA
    # ======================================
    st.subheader("📊 Indicadores de Exposição Consolidados")
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    score_aioe = float(linha_registro.get("AIOE_SCORE", 0.0))
    nivel = linha_registro.get("NIVEL_IMPACTO", "Não informado")
    
    col_kpi1.metric("Índice AIOE (Felten)", f"{score_aioe:.2f}")
    col_kpi2.metric("Classificação de Impacto", nivel)
    
    # Tenta trazer o desvio padrão interno para mostrar a dispersão (Variância de Agregação)
    sd_score = linha_registro.get("SD", 0.0)
    if pd.notna(sd_score) and sd_score > 0:
        col_kpi3.metric("Variância de Agregação (SD)", f"{float(sd_score):.2f}")
    else:
        col_kpi3.metric("Estabilidade do Índice", "Alta Consistência")

    st.divider()

    # ======================================
    # BLOCO 3: COMPOSIÇÃO DE MERCADO HISTÓRICA (PNAD CONTÍNUA)
    # ======================================
    st.subheader("🇧🇷 Retrato Estatístico na Amostra PNAD Contínua")
    st.markdown("Estatísticas agregadas computadas a partir do universo de registros históricos válidos para esta profissão:")

    renda_media = dados_ocupacao["Rendimento_Mensal"].mean()
    idade_media = dados_ocupacao["Idade"].mean()
    
    col_pnad1, col_pnad2, col_pnad3 = st.columns(3)
    
    col_pnad1.metric("💰 Salário Médio Nacional", f"R$ {renda_media:,.2f}" if pd.notna(renda_media) else "Não Amostrado")
    col_pnad2.metric("🎂 Média de Idade dos Ativos", f"{int(idade_media)} anos" if pd.notna(idade_media) else "N/A")
    col_pnad3.metric("👥 Volume de Registros Limpos", f"{len(dados_ocupacao):,} trabalhadores")

    # Distribuição Regional Simplificada por Tabela (Sem gráficos pesados repetidos)
    if "UF" in dados_ocupacao.columns:
        st.write("")
        st.markdown("**Top 5 Estados com Maior Massa Salarial Declarada para esta Profissão:**")
        dist_uf = dados_ocupacao.groupby("UF")["Rendimento_Mensal"].mean().reset_index()
        dist_uf = dist_uf.sort_values(by="Rendimento_Mensal", ascending=False).head(5)
        dist_uf.columns = ["Estado (UF)", "Rendimento Mensal Médio (R$)"]
        st.dataframe(dist_uf, use_container_width=True, hide_index=True)
