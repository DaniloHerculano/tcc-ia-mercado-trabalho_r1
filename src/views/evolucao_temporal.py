import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os


# =============================================================================
# DADOS EXTRAÍDOS DOS GRÁFICOS
# =============================================================================

# --- Evolução trimestral — Felten/AIOE ---
TRIMESTRAL_AIOE = [
    {"periodo": "2020T1", "aioe": -0.140},
    {"periodo": "2020T2", "aioe": -0.080},
    {"periodo": "2020T3", "aioe": -0.073},
    {"periodo": "2020T4", "aioe": -0.097},
    {"periodo": "2021T1", "aioe": -0.085},
    {"periodo": "2021T2", "aioe": -0.063},
    {"periodo": "2021T3", "aioe": -0.110},
    {"periodo": "2021T4", "aioe": -0.121},
    {"periodo": "2022T1", "aioe": -0.139},
    {"periodo": "2022T2", "aioe": -0.140},
    {"periodo": "2022T3", "aioe": -0.123},
    {"periodo": "2022T4", "aioe": -0.119},
    {"periodo": "2023T1", "aioe": -0.120},
    {"periodo": "2023T2", "aioe": -0.110},
    {"periodo": "2023T3", "aioe": -0.088},
    {"periodo": "2023T4", "aioe": -0.091},
    {"periodo": "2024T1", "aioe": -0.085},
    {"periodo": "2024T2", "aioe": -0.073},
    {"periodo": "2024T3", "aioe": -0.080},
    {"periodo": "2024T4", "aioe": -0.098},
    {"periodo": "2025T1", "aioe": -0.073},
    {"periodo": "2025T2", "aioe": -0.097},
    {"periodo": "2025T3", "aioe": -0.075},
    {"periodo": "2025T4", "aioe": -0.055},
]

# --- Evolução trimestral — Gmyrek ---
TRIMESTRAL_GMYREK = [
    {"periodo": "2020T1", "gmyrek": 0.3163},
    {"periodo": "2020T2", "gmyrek": 0.3253},
    {"periodo": "2020T3", "gmyrek": 0.3263},
    {"periodo": "2020T4", "gmyrek": 0.3238},
    {"periodo": "2021T1", "gmyrek": 0.3258},
    {"periodo": "2021T2", "gmyrek": 0.3244},
    {"periodo": "2021T3", "gmyrek": 0.3188},
    {"periodo": "2021T4", "gmyrek": 0.3157},
    {"periodo": "2022T1", "gmyrek": 0.3157},
    {"periodo": "2022T2", "gmyrek": 0.3138},
    {"periodo": "2022T3", "gmyrek": 0.3148},
    {"periodo": "2022T4", "gmyrek": 0.3143},
    {"periodo": "2023T1", "gmyrek": 0.3165},
    {"periodo": "2023T2", "gmyrek": 0.3178},
    {"periodo": "2023T3", "gmyrek": 0.3213},
    {"periodo": "2023T4", "gmyrek": 0.3205},
    {"periodo": "2024T1", "gmyrek": 0.3205},
    {"periodo": "2024T2", "gmyrek": 0.3188},
    {"periodo": "2024T3", "gmyrek": 0.3190},
    {"periodo": "2024T4", "gmyrek": 0.3168},
    {"periodo": "2025T1", "gmyrek": 0.3208},
    {"periodo": "2025T2", "gmyrek": 0.3190},
    {"periodo": "2025T3", "gmyrek": 0.3207},
    {"periodo": "2025T4", "gmyrek": 0.3217},
]

# --- Evolução por gênero — Felten/AIOE ---
GENERO_AIOE = [
    {"ano": 2020, "homem": -0.270, "mulher":  0.155},
    {"ano": 2021, "homem": -0.258, "mulher":  0.138},
    {"ano": 2022, "homem": -0.268, "mulher":  0.075},
    {"ano": 2023, "homem": -0.248, "mulher":  0.098},
    {"ano": 2024, "homem": -0.225, "mulher":  0.118},
    {"ano": 2025, "homem": -0.218, "mulher":  0.122},
]

# --- Evolução por gênero — Gmyrek ---
GENERO_GMYREK = [
    {"ano": 2020, "homem": 0.3168, "mulher": 0.3315},
    {"ano": 2021, "homem": 0.3140, "mulher": 0.3313},
    {"ano": 2022, "homem": 0.3113, "mulher": 0.3198},
    {"ano": 2023, "homem": 0.3163, "mulher": 0.3225},
    {"ano": 2024, "homem": 0.3150, "mulher": 0.3238},
    {"ano": 2025, "homem": 0.3168, "mulher": 0.3252},
]

# --- Composição por gênero — AIOE ---
COMPOSICAO_GENERO = {
    "genero":       ["Homem", "Homem", "Homem", "Mulher", "Mulher", "Mulher"],
    "faixa":        ["baixa exposição", "média exposição", "alta exposição",
                     "baixa exposição", "média exposição", "alta exposição"],
    "percentual":   [33.0, 39.7, 27.5, 31.7, 41.6, 26.7],
}


# =============================================================================
# HELPERS
# =============================================================================

CORES = {"homem": "#4c78a8", "mulher": "#f58518"}
FAIXA_CORES = {
    "baixa exposição": "#4c78a8",
    "média exposição": "#f58518",
    "alta exposição":  "#54a24b",
}


def _line_chart(df, x_col, y_cols, labels, title, y_title, x_title="Período"):
    """Gera um go.Figure de linhas com múltiplas séries."""
    fig = go.Figure()
    cores = [CORES.get(c.lower(), "#888") for c in y_cols]
    for col, cor in zip(y_cols, cores):
        fig.add_trace(go.Scatter(
            x=df[x_col], y=df[col],
            mode="lines+markers",
            name=labels[col],
            line=dict(color=cor, width=2),
            marker=dict(size=7),
            hovertemplate=f"<b>{labels[col]}</b><br>{x_title}: %{{x}}<br>{y_title}: %{{y:.4f}}<extra></extra>",
        ))
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=420,
        hovermode="x unified",
        legend=dict(orientation="v", x=0.82, y=0.98),
        margin=dict(l=10, r=20, t=50, b=60),
        xaxis=dict(tickangle=-45),
    )
    return fig


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def mostrar_evolucao_temporal(df=None):
    st.title("📈 Séries Temporais e Dinâmica Demográfica de Gênero")
    st.markdown("Acompanhe as curvas da exposição à IA no mercado brasileiro (2020–2025).")

    st.info("""
    📖 **Como interpretar esta página**
    
    Esta seção analisa a evolução da exposição ocupacional à Inteligência Artificial ao longo do tempo, permitindo identificar tendências estruturais no mercado de trabalho brasileiro entre 2020 e 2025.
    
    Além da análise temporal agregada, também são apresentados recortes por gênero, possibilitando avaliar como diferentes grupos populacionais podem ser afetados pelas transformações tecnológicas associadas à IA.
    """)
    
    st.divider()

    # =========================================================================
    # SEÇÃO 1: EVOLUÇÃO LONGITUDINAL TRIMESTRAL
    # =========================================================================

    st.markdown("""
    ### ⏳ Evolução da Exposição à IA ao Longo do Tempo
    
    Os gráficos a seguir apresentam a média ponderada dos indicadores de exposição à IA para todas as ocupações observadas na PNAD Contínua.
    
    O objetivo é verificar se a estrutura ocupacional brasileira apresentou mudanças relevantes ao longo do período analisado, especialmente após a aceleração dos investimentos globais em Inteligência Artificial observada nos últimos anos.
    """)
    
    st.subheader("1. Evolução Longitudinal Trimestral")

    df_aioe_t  = pd.DataFrame(TRIMESTRAL_AIOE)
    df_gmy_t   = pd.DataFrame(TRIMESTRAL_GMYREK)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Evolução Trimestral — AIOE")
        fig_t_aioe = go.Figure()
        fig_t_aioe.add_trace(go.Scatter(
            x=df_aioe_t["periodo"], y=df_aioe_t["aioe"],
            mode="lines+markers",
            line=dict(color="#4c78a8", width=2),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>AIOE: %{y:.3f}<extra></extra>",
        ))
        fig_t_aioe.update_layout(
            xaxis_title="Período", yaxis_title="AIOE médio ponderado",
            height=420, showlegend=False,
            margin=dict(l=10, r=20, t=20, b=70),
            xaxis=dict(tickangle=-45),
            hovermode="x",
        )
        st.plotly_chart(fig_t_aioe, use_container_width=True)

        st.success("""
        🔎 **Interpretação dos resultados**
        
        O indicador AIOE apresenta relativa estabilidade ao longo da série histórica, com pequenas oscilações entre os trimestres analisados.
        
        Esse comportamento sugere que a composição ocupacional brasileira não sofreu mudanças abruptas no período, embora seja possível observar uma leve tendência de aproximação a ocupações mais expostas à Inteligência Artificial nos anos mais recentes.
        """)

    with col2:
        st.markdown("#### Evolução Trimestral — Gmyrek")
        fig_t_gmy = go.Figure()
        fig_t_gmy.add_trace(go.Scatter(
            x=df_gmy_t["periodo"], y=df_gmy_t["gmyrek"],
            mode="lines+markers",
            line=dict(color="#4c78a8", width=2),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b><br>Gmyrek: %{y:.4f}<extra></extra>",
        ))
        fig_t_gmy.update_layout(
            xaxis_title="Período", yaxis_title="Mean médio ponderado",
            height=420, showlegend=False,
            margin=dict(l=10, r=20, t=20, b=70),
            xaxis=dict(tickangle=-45),
            hovermode="x",
        )
        st.plotly_chart(fig_t_gmy, use_container_width=True)

        st.success("""
        🔎 **Interpretação dos resultados**
        
        O indicador da OIT (Gmyrek) também apresenta comportamento estável durante o período analisado, reforçando os resultados observados pelo índice AIOE.
        
        A consistência entre os dois referenciais sugere que as transformações observadas decorrem de mudanças graduais na estrutura ocupacional brasileira e não de variações estatísticas ocasionais.
        """)

    st.divider()

    # =========================================================================
    # SEÇÃO 2: RECORTE DE GÊNERO
    # =========================================================================

    st.markdown("""
    ### 👥 Exposição à IA sob a Perspectiva de Gênero
    
    A literatura internacional tem apontado diferenças importantes entre homens e mulheres quanto à exposição ocupacional à Inteligência Artificial.
    
    Os gráficos abaixo investigam se esse comportamento também pode ser observado no mercado de trabalho brasileiro, analisando a evolução dos indicadores ao longo do tempo para cada grupo.
    """)
    
    st.subheader("2. Recorte de Gênero na Exposição")

    df_ga = pd.DataFrame(GENERO_AIOE)
    df_gg = pd.DataFrame(GENERO_GMYREK)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Evolução por Gênero — AIOE")
        fig_ga = _line_chart(
            df_ga, x_col="ano",
            y_cols=["homem", "mulher"],
            labels={"homem": "Homem", "mulher": "Mulher"},
            title="Exposição à IA por gênero — Felten",
            y_title="AIOE médio ponderado",
            x_title="Ano",
        )
        st.plotly_chart(fig_ga, use_container_width=True)

        st.info("""
        📊 **Principais evidências**
        
        Observa-se que as mulheres apresentam níveis médios de exposição superiores aos dos homens durante todo o período analisado.
        
        Esse resultado está associado à maior participação feminina em ocupações administrativas, educacionais, financeiras e de serviços intensivos em informação, atividades frequentemente classificadas como mais suscetíveis à incorporação de ferramentas baseadas em IA.
        """)

    with col4:
        st.markdown("#### Evolução por Gênero — Gmyrek")
        fig_gg = _line_chart(
            df_gg, x_col="ano",
            y_cols=["homem", "mulher"],
            labels={"homem": "Homem", "mulher": "Mulher"},
            title="Exposição à IA por gênero — Gmyrek",
            y_title="Mean médio ponderado",
            x_title="Ano",
        )
        st.plotly_chart(fig_gg, use_container_width=True)

        st.info("""
        📊 **Principais evidências**
        
        Os resultados do indicador Gmyrek confirmam o padrão identificado pelo AIOE, indicando uma exposição relativamente maior entre as mulheres.
        
        A convergência entre os dois referenciais fortalece a hipótese de que os impactos da IA podem ocorrer de forma diferenciada entre grupos demográficos, exigindo atenção em políticas de qualificação profissional e adaptação do mercado de trabalho.
        """)

    st.write("")

    # =========================================================================
    # GRÁFICO 5: COMPOSIÇÃO DE GÊNERO — AIOE
    # =========================================================================

    st.markdown("""
    ### 📌 Distribuição das Ocupações por Faixa de Exposição
    
    Além da evolução temporal, também é importante observar como homens e mulheres estão distribuídos entre as diferentes faixas de exposição à IA.
    
    Essa análise permite identificar se determinados grupos estão mais concentrados em ocupações potencialmente afetadas pelas transformações tecnológicas.
    """)
    
    st.markdown("#### 📊 Composição de Gênero por Faixas de Impacto (AIOE)")

    df_comp = pd.DataFrame(COMPOSICAO_GENERO)

    fig_comp = px.bar(
        df_comp,
        x="genero", y="percentual", color="faixa",
        barmode="group",
        text_auto=".1f",
        color_discrete_map=FAIXA_CORES,
        labels={"genero": "", "percentual": "% dentro do gênero", "faixa": ""},
        category_orders={"faixa": ["baixa exposição", "média exposição", "alta exposição"]},
    )
    fig_comp.update_traces(
        textposition="outside",
        hovertemplate="<b>%{x} — %{data.name}</b><br>%{y:.1f}%<extra></extra>",
    )
    fig_comp.update_layout(
        height=480,
        legend=dict(orientation="v", x=0.82, y=0.98),
        margin=dict(l=10, r=20, t=20, b=40),
        yaxis=dict(range=[0, 50]),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    st.success("""
    🔎 **Interpretação dos resultados**
    
    A distribuição por faixas revela que homens e mulheres possuem participação semelhante nas categorias de média exposição, que concentram a maior parcela das ocupações analisadas.
    
    Entretanto, diferenças aparecem nas extremidades da distribuição, indicando que determinados grupos podem estar mais representados em ocupações com maior ou menor potencial de transformação decorrente da Inteligência Artificial.
    """)

    st.divider()

    st.info("""
    🎯 **Síntese dos resultados**
    
    A análise temporal indica que a exposição à Inteligência Artificial no mercado de trabalho brasileiro evolui de forma gradual e relativamente estável entre 2020 e 2025.
    
    Os resultados também evidenciam diferenças de exposição entre homens e mulheres, sugerindo que os impactos da IA tendem a ocorrer de maneira heterogênea entre grupos ocupacionais e demográficos.
    
    Essas evidências reforçam a importância de políticas voltadas à requalificação profissional e ao desenvolvimento contínuo de competências compatíveis com a crescente incorporação da IA nas atividades econômicas.
    """)
