import streamlit as st
import plotly.express as px
import pandas as pd
import os


# =============================================================================
# DADOS REAIS EXTRAÍDOS DOS GRÁFICOS
# =============================================================================

# --- TOP 20 AIOE (Felten) — escala positiva ~1.05 a 1.50 ---
TOP20_AIOE = [
    {"Ocupação": "PROFISSIONAIS DA ESTATÍSTICA",                                    "Score": 1.50},
    {"Ocupação": "CONTADORES E AUDITORES",                                          "Score": 1.48},
    {"Ocupação": "SERVENTUÁRIOS DA JUSTIÇA E AFINS",                                "Score": 1.46},
    {"Ocupação": "DELEGADOS DE POLÍCIA",                                            "Score": 1.44},
    {"Ocupação": "PROFISSIONAIS DO JORNALISMO",                                     "Score": 1.43},
    {"Ocupação": "PROFISSIONAIS EM PESQUISA E ANÁLISE ANTROPOLÓGICA E SOCIOLÓGICA", "Score": 1.42},
    {"Ocupação": "TÉCNICOS EM TRANSPORTES (ADUANEIROS)",                            "Score": 1.42},
    {"Ocupação": "PROFISSIONAIS EM PESQUISA E ANÁLISE ECONÔMICA",                   "Score": 1.42},
    {"Ocupação": "ADMINISTRADORES",                                                 "Score": 1.40},
    {"Ocupação": "FÍSICOS",                                                         "Score": 1.39},
    {"Ocupação": "ENGENHEIROS QUÍMICOS",                                            "Score": 1.37},
    {"Ocupação": "ENGENHEIROS MECÂNICOS",                                           "Score": 1.36},
    {"Ocupação": "FILÓSOFOS E CIENTISTAS POLÍTICOS",                                "Score": 1.35},
    {"Ocupação": "INSPETORES DE ALUNOS E AFINS",                                    "Score": 1.33},
    {"Ocupação": "MINISTROS DE CULTOS RELIGIOSOS, MISSIONÁRIOS E AFINS",            "Score": 1.31},
    {"Ocupação": "COLETADORES DE APOSTAS E DE JOGOS",                               "Score": 1.28},
    {"Ocupação": "CAIXAS DE BANCO E OPERADORES DE CÂMBIO",                          "Score": 1.24},
    {"Ocupação": "ENGENHEIROS ELETROELETRÔNICOS E AFINS",                           "Score": 1.24},
    {"Ocupação": "OPERADORES DE TELEMARKETING",                                     "Score": 1.22},
    {"Ocupação": "ARQUITETOS",                                                      "Score": 1.06},
]

# --- BOTTOM 20 AIOE (Felten) — escala negativa ~-1.6 a 0.0 ---
BOT20_AIOE = [
    {"Ocupação": "TRABALHADORES DE MOLDAGEM DE METAIS E DE COMPÓSITOS",                                         "Score": -1.60},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE PEDRAS",                                                   "Score": -1.58},
    {"Ocupação": "GARIMPEIROS E OPERADORES DE SALINAS",                                                         "Score": -1.40},
    {"Ocupação": "TRABALHADORES NOS SERVIÇOS DE MANUTENÇÃO E CONSERVAÇÃO DE EDIFÍCIOS E LOGRADOUROS",           "Score": -1.35},
    {"Ocupação": "TRABALHADORES DA EXTRAÇÃO DE MINERAIS LÍQUIDOS E GASOSOS",                                    "Score": -1.30},
    {"Ocupação": "TRABALHADORES DE TRATAMENTO TÉRMICO DE METAIS E DE COMPÓSITOS",                               "Score": -1.10},
    {"Ocupação": "TRABALHADORES DE FUNDIÇÃO DE METAIS E DE COMPÓSITOS",                                         "Score": -1.05},
    {"Ocupação": "OPERADORES DE FORNOS DE 1ª FUSÃO E ACIARIA",                                                  "Score": -1.00},
    {"Ocupação": "TRABALHADORES DE TREFILAÇÃO, ESTIRAMENTO E EXTRUSÃO DE METAIS E DE COMPÓSITOS",               "Score": -0.95},
    {"Ocupação": "SOPRADORES E MOLDADORES DE VIDROS E AFINS",                                                   "Score": -0.90},
    {"Ocupação": "TRABALHADORES DA PINTURA DE EQUIPAMENTOS, VEÍCULOS, ESTRUTURAS METÁLICAS E DE COMPÓSITOS",   "Score": -0.85},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE MINÉRIOS",                                                 "Score": -0.75},
    {"Ocupação": "CERAMISTAS (PREPARAÇÃO E FABRICAÇÃO)",                                                        "Score": -0.70},
    {"Ocupação": "OPERADORES DE USINAGEM CONVENCIONAL (PRODUÇÃO EM SÉRIE)",                                     "Score": -0.65},
    {"Ocupação": "TRABALHADORES DE FORJAMENTO DE METAIS",                                                       "Score": -0.60},
    {"Ocupação": "TRABALHADORES DOS SERVIÇOS FUNERÁRIOS",                                                       "Score": -0.55},
    {"Ocupação": "VENDEDORES EM QUIOSQUES E BARRACAS",                                                          "Score": -0.50},
    {"Ocupação": "ATENDENTES DE ENFERMAGEM, PARTEIRAS PRÁTICAS E AFINS",                                        "Score": -0.45},
    {"Ocupação": "PREPARADORES E OPERADORES DE MÁQUINAS - FERRAMENTA CONVENCIONAL",                             "Score": -0.40},
    {"Ocupação": "TÉCNICOS E AUXILIARES DE ENFERMAGEM",                                                         "Score": -0.35},
]

# --- TOP 20 GMYREK — escala 0.37 a 0.59 ---
TOP20_GMYREK = [
    {"Ocupação": "FILÓSOFOS E CIENTISTAS POLÍTICOS",                                "Score": 0.590},
    {"Ocupação": "CAIXAS E BILHETEIROS (EXCETO CAIXAS DE BANCO)",                   "Score": 0.585},
    {"Ocupação": "ADMINISTRADORES",                                                 "Score": 0.575},
    {"Ocupação": "TÉCNICOS EM TRANSPORTES (ADUANEIROS)",                            "Score": 0.570},
    {"Ocupação": "PROFISSIONAIS DA ESTATÍSTICA",                                    "Score": 0.565},
    {"Ocupação": "PROFISSIONAIS DA INFORMAÇÃO",                                     "Score": 0.555},
    {"Ocupação": "PROFISSIONAIS DO JORNALISMO",                                     "Score": 0.550},
    {"Ocupação": "PROFISSIONAIS EM PESQUISA E ANÁLISE ECONÔMICA",                   "Score": 0.548},
    {"Ocupação": "CONTADORES E AUDITORES",                                          "Score": 0.510},
    {"Ocupação": "PROFISSIONAIS EM PESQUISA E ANÁLISE ANTROPOLÓGICA E SOCIOLÓGICA", "Score": 0.475},
    {"Ocupação": "OPERADORES DE TELEMARKETING",                                     "Score": 0.460},
    {"Ocupação": "CAIXAS DE BANCO E OPERADORES DE CÂMBIO",                          "Score": 0.450},
    {"Ocupação": "ESCRITURÁRIOS EM GERAL, AGENTES, ASSISTENTES E AUXILIARES ADMINISTRATIVOS", "Score": 0.430},
    {"Ocupação": "TÉCNICOS EM TRANSPORTES RODOVIÁRIOS",                             "Score": 0.425},
    {"Ocupação": "TÉCNICOS EM CONTABILIDADE",                                       "Score": 0.422},
    {"Ocupação": "COLETADORES DE APOSTAS E DE JOGOS",                               "Score": 0.420},
    {"Ocupação": "TELEFONISTAS",                                                    "Score": 0.415},
    {"Ocupação": "SERVENTUÁRIOS DA JUSTIÇA E AFINS",                                "Score": 0.400},
    {"Ocupação": "INSPETORES DE ALUNOS E AFINS",                                    "Score": 0.395},
    {"Ocupação": "FÍSICOS",                                                         "Score": 0.375},
]

# --- BOTTOM 20 GMYREK — escala 0.07 a 0.21 ---
BOT20_GMYREK = [
    {"Ocupação": "TRABALHADORES NOS SERVIÇOS DE ADMINISTRAÇÃO DE EDIFÍCIOS",                          "Score": 0.090},
    {"Ocupação": "GARIMPEIROS E OPERADORES DE SALINAS",                                               "Score": 0.100},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE PEDRAS",                                         "Score": 0.102},
    {"Ocupação": "TRABALHADORES NOS SERVIÇOS DE MANUTENÇÃO E CONSERVAÇÃO DE EDIFÍCIOS E LOGRADOUROS", "Score": 0.110},
    {"Ocupação": "TRABALHADORES DE MOLDAGEM DE METAIS E DE COMPÓSITOS",                               "Score": 0.118},
    {"Ocupação": "CONFECCIONADORES DE INSTRUMENTOS MUSICAIS",                                         "Score": 0.130},
    {"Ocupação": "INSTALADORES E REPARADORES DE LINHAS E CABOS ELÉTRICOS, TELEFÔNICOS E DE COMUNICAÇÃO DE DADOS", "Score": 0.145},
    {"Ocupação": "TRABALHADORES DE FORJAMENTO DE METAIS",                                             "Score": 0.175},
    {"Ocupação": "TRABALHADORES DOS SERVIÇOS FUNERÁRIOS",                                             "Score": 0.178},
    {"Ocupação": "TRABALHADORES NOS SERVIÇOS DE HIGIENE E EMBELEZAMENTO",                             "Score": 0.180},
    {"Ocupação": "OPERADORES DE USINAGEM CONVENCIONAL (PRODUÇÃO EM SÉRIE)",                           "Score": 0.181},
    {"Ocupação": "MINISTROS DE CULTOS RELIGIOSOS, MISSIONÁRIOS E AFINS",                              "Score": 0.183},
    {"Ocupação": "PREPARADORES E OPERADORES DE MÁQUINAS - FERRAMENTA CONVENCIONAL",                   "Score": 0.190},
    {"Ocupação": "CERAMISTAS (PREPARAÇÃO E FABRICAÇÃO)",                                              "Score": 0.195},
    {"Ocupação": "PRODUTORES AGRÍCOLAS",                                                              "Score": 0.197},
    {"Ocupação": "ATENDENTES DE CRECHE E ACOMPANHANTES DE IDOSOS",                                    "Score": 0.200},
    {"Ocupação": "SOPRADORES E MOLDADORES DE VIDROS E AFINS",                                         "Score": 0.202},
    {"Ocupação": "TRABALHADORES DA EXTRAÇÃO DE MINERAIS LÍQUIDOS E GASOSOS",                          "Score": 0.205},
    {"Ocupação": "PROFESSORES NA EDUCAÇÃO INFANTIL (COM FORMAÇÃO DE NÍVEL MÉDIO)",                    "Score": 0.210},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE MINÉRIOS",                                       "Score": 0.215},
]


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

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
    # ABA 1: DISPERSÃO E REGRESSÃO (IMAGENS ESTÁTICAS — mantidas como estão)
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
    # ABA 2: RANKINGS EXTREMOS — GRÁFICOS INTERATIVOS PLOTLY
    # =========================================================================
    with tab_rankings:
        st.subheader("Classificação dos Extremos de Exposição")
        modelo = st.radio(
            "Selecione o referencial teórico:",
            ["Indicador AIOE (Felten)", "Indicador Gmyrek / OIT"],
            horizontal=True,
        )
        st.write("")

        if "AIOE" in modelo:
            df_top = pd.DataFrame(TOP20_AIOE)
            df_bot = pd.DataFrame(BOT20_AIOE)
            x_label_top = "Felten/AIOE"
            x_label_bot = "Felten/AIOE"
            color_top = "Reds"
            color_bot = "Blues"
            title_top = "🚨 Top 20 Ocupações Mais Expostas — Felten/AIOE"
            title_bot = "🟢 Bottom 20 Ocupações Menos Expostas — Felten/AIOE"
        else:
            df_top = pd.DataFrame(TOP20_GMYREK)
            df_bot = pd.DataFrame(BOT20_GMYREK)
            x_label_top = "Gmyrek Mean"
            x_label_bot = "Gmyrek Mean"
            color_top = "Oranges"
            color_bot = "Blues"
            title_top = "🚨 Top 20 Ocupações Mais Expostas — Gmyrek Mean"
            title_bot = "🟢 Bottom 20 Ocupações Menos Expostas — Gmyrek Mean"

        # ---- TOP 20 ----
        st.markdown(f"#### {title_top}")
        df_top_sorted = df_top.sort_values("Score", ascending=True)

        fig_top = px.bar(
            df_top_sorted,
            x="Score",
            y="Ocupação",
            orientation="h",
            text_auto=".2f",
            color="Score",
            color_continuous_scale=color_top,
            labels={"Score": x_label_top, "Ocupação": ""},
        )
        fig_top.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
        )
        fig_top.update_layout(
            height=700,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=20, b=40),
            xaxis_title=x_label_top,
            yaxis_title="",
            font=dict(size=11),
        )
        st.plotly_chart(fig_top, use_container_width=True)

        st.divider()

        # ---- BOTTOM 20 ----
        st.markdown(f"#### {title_bot}")
        df_bot_sorted = df_bot.sort_values("Score", ascending=False)

        fig_bot = px.bar(
            df_bot_sorted,
            x="Score",
            y="Ocupação",
            orientation="h",
            text_auto=".2f",
            color="Score",
            color_continuous_scale=color_bot,
            labels={"Score": x_label_bot, "Ocupação": ""},
        )
        fig_bot.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
        )
        fig_bot.update_layout(
            height=700,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=20, b=40),
            xaxis_title=x_label_bot,
            yaxis_title="",
            font=dict(size=11),
        )
        st.plotly_chart(fig_bot, use_container_width=True)
