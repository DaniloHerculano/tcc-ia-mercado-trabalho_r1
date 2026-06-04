import streamlit as st
import plotly.express as px


# ==========================================
# SIMILARIDADE
# ==========================================

def mostrar_similaridade(df):

    st.title(
        "🧠 Similaridade Semântica"
    )

    st.markdown("""
    Correspondência semântica entre
    ocupações brasileiras (CBO)
    e ocupações americanas
    do dataset AIOE/Felten.
    """)

    st.warning("""
    Os testes de similaridade semântica foram realizados como etapa complementar de apoio ao processo de harmonização ocupacional.
    
    Os resultados apresentaram níveis moderados de correspondência, motivo pelo qual os indicadores finais utilizados neste estudo foram priorizados a partir de métodos estruturados de compatibilização ocupacional.
    """)
    
    st.info("""
    Esta etapa foi utilizada para associar ocupações brasileiras da CBO às ocupações presentes na base internacional de Felten et al. (2023).

    Como as nomenclaturas entre os sistemas ocupacionais não são idênticas, foi aplicada uma estratégia de similaridade semântica baseada em embeddings de linguagem natural.

    Dessa forma, foi possível avaliar o potencial de correspondência entre ocupações brasileiras e internacionais por meio de similaridade semântica.

    Os resultados serviram como apoio exploratório à etapa de harmonização ocupacional, mas não foram utilizados como critério principal para construção da base final devido aos níveis moderados de similaridade observados.
    """)

    st.divider()

    # ======================================
    # HISTOGRAMA
    # ======================================

    fig = px.histogram(
        df,
        x="AIOE_SCORE",
        nbins=30,
        title="Distribuição dos Scores AIOE"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success("""
    Interpretação:

    A distribuição demonstra como os indicadores AIOE ficaram distribuídos entre as ocupações brasileiras após o processo de compatibilização semântica.

    Valores mais elevados indicam ocupações potencialmente mais expostas à automação baseada em Inteligência Artificial, enquanto valores menores sugerem atividades menos suscetíveis à substituição ou complementação por tecnologias generativas.

    A concentração dos valores permite avaliar se o impacto da IA está distribuído de forma homogênea ou concentrado em grupos específicos de ocupações.
    """)

    st.divider()

    # ======================================
    # EXEMPLOS DE MATCH SEMÂNTICO
    # ======================================

    st.subheader("🎯 Exemplos de Correspondência Semântica")

    top_matches = (
        df[
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
                "AIOE_SCORE"
            ]
        ]
        .sort_values(
            "AIOE_SCORE",
            ascending=False
        )
        .head(10)
    )

    fig_match = px.bar(
        top_matches.sort_values(
            "AIOE_SCORE",
            ascending=True
        ),
        x="AIOE_SCORE",
        y="TITULO_LIMPO",
        orientation="h",
        text="AIOE_SCORE",
        hover_data=["AIOE_MATCH_TITLE"],
        color="AIOE_SCORE",
        color_continuous_scale="Blues"
    )

    fig_match.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_match.update_layout(
        height=500,
        coloraxis_showscale=False,
        xaxis_title="Score AIOE",
        yaxis_title="Ocupação Brasileira"
    )

    st.plotly_chart(
        fig_match,
        use_container_width=True
    )

    st.info("""
    O gráfico apresenta exemplos de ocupações brasileiras associadas às ocupações da base internacional de Felten por meio de similaridade semântica.

    Quanto maior o score observado, maior a proximidade entre a descrição da ocupação brasileira e sua correspondente internacional. Isso aumenta a confiança na transferência dos indicadores de exposição à Inteligência Artificial utilizados ao longo deste estudo.

    Passe o mouse sobre cada barra para visualizar a ocupação correspondente encontrada na base internacional.
    """)

    st.divider()

    # ======================================
    # TOP MATCHES
    # ======================================

    st.subheader(
        "🔥 Ocupações Mais Expostas"
    )

    top = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=False
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
                "AIOE_SCORE"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        top,
        use_container_width=True
    )

    st.info("""
    As ocupações listadas acima representam os maiores níveis de exposição à IA segundo a metodologia AIOE.

    Em geral, aparecem atividades intensivas em processamento de informação, análise de dados, produção de conteúdo, elaboração de documentos e tomada de decisão baseada em conhecimento. Essas características tendem a ser mais facilmente complementadas ou automatizadas por modelos modernos de Inteligência Artificial.
    """)

    st.divider()

    # ======================================
    # BAIXA EXPOSIÇÃO
    # ======================================

    st.subheader(
        "⚠️ Ocupações Menos Expostas"
    )

    baixo = (
        df.sort_values(
            by="AIOE_SCORE",
            ascending=True
        )
        [
            [
                "TITULO_LIMPO",
                "AIOE_MATCH_TITLE",
                "AIOE_SCORE"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        baixo,
        use_container_width=True
    )

    st.info("""
    As ocupações com menores scores de exposição costumam envolver atividades predominantemente manuais, físicas ou dependentes de interação presencial.

    Essas funções normalmente apresentam menor potencial de automação por ferramentas de IA generativa, exigindo habilidades motoras, operação de equipamentos ou atuação em ambientes físicos complexos.
    """)

    st.divider()

    # ======================================
    # MÉTRICAS
    # ======================================

    media = round(
        df["AIOE_SCORE"].mean(),
        3
    )

    maior = round(
        df["AIOE_SCORE"].max(),
        3
    )

    menor = round(
        df["AIOE_SCORE"].min(),
        3
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Média",
        media
    )

    col2.metric(
        "Maior Score",
        maior
    )

    col3.metric(
        "Menor Score",
        menor
    )

    st.success(f"""
    Resumo dos resultados:

    • Score médio observado: {media}

    • Maior exposição identificada: {maior}

    • Menor exposição identificada: {menor}

    Esses indicadores fornecem uma visão consolidada do grau de exposição à IA presente no conjunto de ocupações analisadas. A amplitude observada entre os valores mínimo e máximo evidencia que o impacto potencial da Inteligência Artificial não ocorre de forma uniforme entre as diferentes profissões.
    """)
