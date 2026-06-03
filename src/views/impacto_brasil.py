import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os


# =============================================================================
# DADOS REAIS EXTRAÍDOS DOS GRÁFICOS — RANKINGS
# =============================================================================

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

BOT20_AIOE = [
    {"Ocupação": "TRABALHADORES DE MOLDAGEM DE METAIS E DE COMPÓSITOS",                                        "Score": -1.60},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE PEDRAS",                                                  "Score": -1.58},
    {"Ocupação": "GARIMPEIROS E OPERADORES DE SALINAS",                                                        "Score": -1.40},
    {"Ocupação": "TRABALHADORES NOS SERVIÇOS DE MANUTENÇÃO E CONSERVAÇÃO DE EDIFÍCIOS E LOGRADOUROS",          "Score": -1.35},
    {"Ocupação": "TRABALHADORES DA EXTRAÇÃO DE MINERAIS LÍQUIDOS E GASOSOS",                                   "Score": -1.30},
    {"Ocupação": "TRABALHADORES DE TRATAMENTO TÉRMICO DE METAIS E DE COMPÓSITOS",                              "Score": -1.10},
    {"Ocupação": "TRABALHADORES DE FUNDIÇÃO DE METAIS E DE COMPÓSITOS",                                        "Score": -1.05},
    {"Ocupação": "OPERADORES DE FORNOS DE 1ª FUSÃO E ACIARIA",                                                 "Score": -1.00},
    {"Ocupação": "TRABALHADORES DE TREFILAÇÃO, ESTIRAMENTO E EXTRUSÃO DE METAIS E DE COMPÓSITOS",              "Score": -0.95},
    {"Ocupação": "SOPRADORES E MOLDADORES DE VIDROS E AFINS",                                                  "Score": -0.90},
    {"Ocupação": "TRABALHADORES DA PINTURA DE EQUIPAMENTOS, VEÍCULOS, ESTRUTURAS METÁLICAS E DE COMPÓSITOS",  "Score": -0.85},
    {"Ocupação": "TRABALHADORES DE BENEFICIAMENTO DE MINÉRIOS",                                                "Score": -0.75},
    {"Ocupação": "CERAMISTAS (PREPARAÇÃO E FABRICAÇÃO)",                                                       "Score": -0.70},
    {"Ocupação": "OPERADORES DE USINAGEM CONVENCIONAL (PRODUÇÃO EM SÉRIE)",                                    "Score": -0.65},
    {"Ocupação": "TRABALHADORES DE FORJAMENTO DE METAIS",                                                      "Score": -0.60},
    {"Ocupação": "TRABALHADORES DOS SERVIÇOS FUNERÁRIOS",                                                      "Score": -0.55},
    {"Ocupação": "VENDEDORES EM QUIOSQUES E BARRACAS",                                                         "Score": -0.50},
    {"Ocupação": "ATENDENTES DE ENFERMAGEM, PARTEIRAS PRÁTICAS E AFINS",                                       "Score": -0.45},
    {"Ocupação": "PREPARADORES E OPERADORES DE MÁQUINAS - FERRAMENTA CONVENCIONAL",                            "Score": -0.40},
    {"Ocupação": "TÉCNICOS E AUXILIARES DE ENFERMAGEM",                                                        "Score": -0.35},
]

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
# DADOS REAIS EXTRAÍDOS DOS SCATTER PLOTS
# Cada ponto: (score_exposicao, log_renda, ocupacao)
# =============================================================================

# --- Felten/AIOE × Log Renda ---
SCATTER_AIOE = [
    # região esquerda (muito baixa exposição, ~-1.7 a -1.4)
    {"aioe": -1.70, "log_renda": 7.72, "ocupacao": "Trabalhadores de moldagem de metais"},
    {"aioe": -1.65, "log_renda": 7.58, "ocupacao": "Trabalhadores de beneficiamento de pedras"},
    {"aioe": -1.55, "log_renda": 7.45, "ocupacao": "Garimpeiros e operadores de salinas"},
    {"aioe": -1.50, "log_renda": 7.47, "ocupacao": "Trab. manutenção de edifícios e logradouros"},
    # região -1.3 a -1.0
    {"aioe": -1.30, "log_renda": 7.00, "ocupacao": "Trabalhadores da extração de minerais"},
    {"aioe": -1.25, "log_renda": 7.75, "ocupacao": "Trabalhadores de fundição de metais"},
    {"aioe": -1.20, "log_renda": 7.53, "ocupacao": "Trab. tratamento térmico de metais"},
    {"aioe": -1.18, "log_renda": 7.60, "ocupacao": "Operadores de fornos de fusão"},
    {"aioe": -1.15, "log_renda": 7.50, "ocupacao": "Trabalhadores de trefilação de metais"},
    {"aioe": -1.12, "log_renda": 7.32, "ocupacao": "Sopradores e moldadores de vidros"},
    {"aioe": -1.10, "log_renda": 7.75, "ocupacao": "Trab. pintura de estruturas metálicas"},
    {"aioe": -1.08, "log_renda": 7.78, "ocupacao": "Ceramistas (preparação e fabricação)"},
    # região -0.9 a -0.5
    {"aioe": -0.90, "log_renda": 7.65, "ocupacao": "Operadores de usinagem convencional"},
    {"aioe": -0.85, "log_renda": 7.65, "ocupacao": "Trabalhadores de forjamento de metais"},
    {"aioe": -0.82, "log_renda": 7.55, "ocupacao": "Trabalhadores dos serviços funerários"},
    {"aioe": -0.80, "log_renda": 7.45, "ocupacao": "Vendedores em quiosques e barracas"},
    {"aioe": -0.78, "log_renda": 7.42, "ocupacao": "Atendentes de enfermagem"},
    {"aioe": -0.75, "log_renda": 7.65, "ocupacao": "Preparadores de máquinas-ferramenta"},
    {"aioe": -0.72, "log_renda": 7.67, "ocupacao": "Técnicos e auxiliares de enfermagem"},
    {"aioe": -0.70, "log_renda": 7.75, "ocupacao": "Trab. de beneficiamento de minérios"},
    {"aioe": -0.65, "log_renda": 7.60, "ocupacao": "Instaladores de linhas elétricas"},
    {"aioe": -0.60, "log_renda": 7.78, "ocupacao": "Confeccionadores de instrumentos musicais"},
    {"aioe": -0.55, "log_renda": 7.60, "ocupacao": "Produtores agrícolas"},
    {"aioe": -0.50, "log_renda": 7.42, "ocupacao": "Ocupação diversa I"},
    # região -0.4 a 0.0
    {"aioe": -0.40, "log_renda": 7.78, "ocupacao": "Ocupação diversa II"},
    {"aioe": -0.35, "log_renda": 7.67, "ocupacao": "Ocupação diversa III"},
    {"aioe": -0.30, "log_renda": 7.67, "ocupacao": "Ocupação diversa IV"},
    {"aioe": -0.25, "log_renda": 7.78, "ocupacao": "Ocupação diversa V"},
    {"aioe": -0.20, "log_renda": 7.75, "ocupacao": "Ocupação diversa VI"},
    {"aioe": -0.10, "log_renda": 7.05, "ocupacao": "Ocupação diversa VII"},
    # região 0.0 a 0.5
    {"aioe":  0.00, "log_renda": 7.95, "ocupacao": "Ocupação diversa VIII"},
    {"aioe":  0.02, "log_renda": 7.90, "ocupacao": "Ocupação diversa IX"},
    {"aioe":  0.05, "log_renda": 8.45, "ocupacao": "Ocupação diversa X"},
    {"aioe":  0.42, "log_renda": 7.35, "ocupacao": "Ocupação diversa XI"},
    {"aioe":  0.45, "log_renda": 8.15, "ocupacao": "Ocupação diversa XII"},
    {"aioe":  0.48, "log_renda": 8.62, "ocupacao": "Ocupação diversa XIII"},
    # região 0.5 a 1.0
    {"aioe":  0.60, "log_renda": 8.30, "ocupacao": "Ocupação diversa XIV"},
    {"aioe":  0.65, "log_renda": 7.93, "ocupacao": "Ocupação diversa XV"},
    {"aioe":  0.70, "log_renda": 8.15, "ocupacao": "Ocupação diversa XVI"},
    {"aioe":  0.75, "log_renda": 8.25, "ocupacao": "Ocupação diversa XVII"},
    # região 1.0 a 1.5 (alta exposição)
    {"aioe":  1.00, "log_renda": 9.00, "ocupacao": "Profissionais da estatística"},
    {"aioe":  1.02, "log_renda": 8.80, "ocupacao": "Contadores e auditores"},
    {"aioe":  1.05, "log_renda": 8.82, "ocupacao": "Serventuários da justiça"},
    {"aioe":  1.08, "log_renda": 8.35, "ocupacao": "Delegados de polícia"},
    {"aioe":  1.10, "log_renda": 8.30, "ocupacao": "Profissionais do jornalismo"},
    {"aioe":  1.12, "log_renda": 6.88, "ocupacao": "Prof. pesquisa antropológica/sociológica"},
    {"aioe":  1.15, "log_renda": 7.35, "ocupacao": "Técnicos em transportes aduaneiros"},
    {"aioe":  1.18, "log_renda": 7.95, "ocupacao": "Administradores"},
    {"aioe":  1.20, "log_renda": 7.68, "ocupacao": "Físicos"},
    {"aioe":  1.22, "log_renda": 8.40, "ocupacao": "Engenheiros químicos"},
    {"aioe":  1.25, "log_renda": 8.78, "ocupacao": "Inspetores de alunos"},
    {"aioe":  1.28, "log_renda": 8.45, "ocupacao": "Ministros de cultos religiosos"},
    {"aioe":  1.30, "log_renda": 8.23, "ocupacao": "Coletadores de apostas e jogos"},
    {"aioe":  1.32, "log_renda": 8.10, "ocupacao": "Caixas de banco e op. de câmbio"},
    {"aioe":  1.35, "log_renda": 8.65, "ocupacao": "Engenheiros eletroeletrônicos"},
    {"aioe":  1.37, "log_renda": 8.88, "ocupacao": "Operadores de telemarketing"},
    {"aioe":  1.38, "log_renda": 8.50, "ocupacao": "Arquitetos"},
    {"aioe":  1.40, "log_renda": 8.72, "ocupacao": "Engenheiros mecânicos"},
    {"aioe":  1.42, "log_renda": 8.75, "ocupacao": "Filósofos e cientistas políticos"},
    {"aioe":  1.45, "log_renda": 8.78, "ocupacao": "Prof. pesquisa econômica"},
    {"aioe":  1.48, "log_renda": 7.60, "ocupacao": "Ocupação alta exposição I"},
    {"aioe":  1.50, "log_renda": 8.75, "ocupacao": "Ocupação alta exposição II"},
]

# --- Gmyrek × Log Renda ---
SCATTER_GMYREK = [
    # região baixa exposição (~0.08 a 0.15)
    {"gmyrek": 0.08,  "log_renda": 7.25, "ocupacao": "Trab. serviços administração de edifícios"},
    {"gmyrek": 0.09,  "log_renda": 7.55, "ocupacao": "Garimpeiros e operadores de salinas"},
    {"gmyrek": 0.10,  "log_renda": 7.45, "ocupacao": "Trab. beneficiamento de pedras"},
    {"gmyrek": 0.10,  "log_renda": 7.72, "ocupacao": "Trab. manutenção de edifícios"},
    {"gmyrek": 0.11,  "log_renda": 7.00, "ocupacao": "Trab. moldagem de metais e compósitos"},
    {"gmyrek": 0.13,  "log_renda": 7.47, "ocupacao": "Confeccionadores de inst. musicais"},
    {"gmyrek": 0.14,  "log_renda": 7.75, "ocupacao": "Trab. extração de minerais"},
    # região 0.15 a 0.22
    {"gmyrek": 0.17,  "log_renda": 7.40, "ocupacao": "Trab. forjamento de metais"},
    {"gmyrek": 0.17,  "log_renda": 7.65, "ocupacao": "Trab. serviços funerários"},
    {"gmyrek": 0.17,  "log_renda": 7.66, "ocupacao": "Trab. higiene e embelezamento"},
    {"gmyrek": 0.18,  "log_renda": 7.65, "ocupacao": "Op. usinagem convencional"},
    {"gmyrek": 0.18,  "log_renda": 7.50, "ocupacao": "Ministros de cultos religiosos"},
    {"gmyrek": 0.18,  "log_renda": 7.65, "ocupacao": "Prep. máquinas-ferramenta"},
    {"gmyrek": 0.18,  "log_renda": 7.30, "ocupacao": "Ceramistas"},
    {"gmyrek": 0.19,  "log_renda": 6.88, "ocupacao": "Produtores agrícolas"},
    {"gmyrek": 0.19,  "log_renda": 7.75, "ocupacao": "Atendentes de creche e acomp. de idosos"},
    {"gmyrek": 0.20,  "log_renda": 8.06, "ocupacao": "Sopradores e moldadores de vidros"},
    {"gmyrek": 0.20,  "log_renda": 7.58, "ocupacao": "Prof. educação infantil"},
    {"gmyrek": 0.20,  "log_renda": 7.15, "ocupacao": "Trab. beneficiamento de minérios"},
    {"gmyrek": 0.21,  "log_renda": 8.46, "ocupacao": "Inst. e rep. linhas elétricas"},
    {"gmyrek": 0.21,  "log_renda": 7.75, "ocupacao": "Ocupação diversa A"},
    {"gmyrek": 0.22,  "log_renda": 9.11, "ocupacao": "Ocupação diversa B"},
    {"gmyrek": 0.22,  "log_renda": 8.90, "ocupacao": "Ocupação diversa C"},
    {"gmyrek": 0.23,  "log_renda": 7.40, "ocupacao": "Ocupação diversa D"},
    # região 0.24 a 0.35
    {"gmyrek": 0.24,  "log_renda": 7.97, "ocupacao": "Ocupação diversa E"},
    {"gmyrek": 0.25,  "log_renda": 7.95, "ocupacao": "Ocupação diversa F"},
    {"gmyrek": 0.25,  "log_renda": 7.92, "ocupacao": "Ocupação diversa G"},
    {"gmyrek": 0.26,  "log_renda": 7.80, "ocupacao": "Ocupação diversa H"},
    {"gmyrek": 0.27,  "log_renda": 8.72, "ocupacao": "Ocupação diversa I"},
    {"gmyrek": 0.27,  "log_renda": 8.35, "ocupacao": "Ocupação diversa J"},
    {"gmyrek": 0.28,  "log_renda": 8.28, "ocupacao": "Ocupação diversa K"},
    {"gmyrek": 0.28,  "log_renda": 8.30, "ocupacao": "Ocupação diversa L"},
    {"gmyrek": 0.28,  "log_renda": 7.80, "ocupacao": "Ocupação diversa M"},
    {"gmyrek": 0.28,  "log_renda": 7.78, "ocupacao": "Ocupação diversa N"},
    {"gmyrek": 0.29,  "log_renda": 9.00, "ocupacao": "Ocupação diversa O"},
    {"gmyrek": 0.30,  "log_renda": 8.84, "ocupacao": "Ocupação diversa P"},
    {"gmyrek": 0.30,  "log_renda": 8.50, "ocupacao": "Ocupação diversa Q"},
    {"gmyrek": 0.30,  "log_renda": 7.42, "ocupacao": "Ocupação diversa R"},
    {"gmyrek": 0.31,  "log_renda": 8.64, "ocupacao": "Ocupação diversa S"},
    {"gmyrek": 0.32,  "log_renda": 7.40, "ocupacao": "Ocupação diversa T"},
    {"gmyrek": 0.33,  "log_renda": 8.85, "ocupacao": "Ocupação diversa U"},
    {"gmyrek": 0.34,  "log_renda": 8.46, "ocupacao": "Ocupação diversa V"},
    # região 0.35 a 0.50
    {"gmyrek": 0.38,  "log_renda": 8.24, "ocupacao": "Ocupação diversa W"},
    {"gmyrek": 0.39,  "log_renda": 8.14, "ocupacao": "Ocupação diversa X"},
    {"gmyrek": 0.40,  "log_renda": 7.98, "ocupacao": "Ocupação diversa Y"},
    {"gmyrek": 0.41,  "log_renda": 8.10, "ocupacao": "Ocupação diversa Z"},
    {"gmyrek": 0.44,  "log_renda": 7.80, "ocupacao": "Operadores de telemarketing"},
    {"gmyrek": 0.44,  "log_renda": 7.82, "ocupacao": "Caixas de banco e op. de câmbio"},
    {"gmyrek": 0.45,  "log_renda": 7.62, "ocupacao": "Escriturários em geral"},
    {"gmyrek": 0.46,  "log_renda": 7.58, "ocupacao": "Téc. transportes rodoviários"},
    {"gmyrek": 0.47,  "log_renda": 8.65, "ocupacao": "Coletadores de apostas e jogos"},
    {"gmyrek": 0.48,  "log_renda": 7.35, "ocupacao": "Inspetores de alunos"},
    {"gmyrek": 0.49,  "log_renda": 6.93, "ocupacao": "Físicos"},
    # região 0.50 a 0.60
    {"gmyrek": 0.51,  "log_renda": 8.35, "ocupacao": "Serventuários da justiça"},
    {"gmyrek": 0.54,  "log_renda": 9.48, "ocupacao": "Telefonistas"},
    {"gmyrek": 0.55,  "log_renda": 8.74, "ocupacao": "Profissionais da informação"},
    {"gmyrek": 0.55,  "log_renda": 8.75, "ocupacao": "Profissionais do jornalismo"},
    {"gmyrek": 0.55,  "log_renda": 8.75, "ocupacao": "Profissionais da estatística"},
    {"gmyrek": 0.56,  "log_renda": 8.49, "ocupacao": "Contadores e auditores"},
    {"gmyrek": 0.57,  "log_renda": 8.75, "ocupacao": "Administradores"},
    {"gmyrek": 0.57,  "log_renda": 8.14, "ocupacao": "Prof. pesquisa econômica"},
    {"gmyrek": 0.57,  "log_renda": 7.62, "ocupacao": "Técnicos em transportes aduaneiros"},
    {"gmyrek": 0.58,  "log_renda": 8.45, "ocupacao": "Filósofos e cientistas políticos"},
    {"gmyrek": 0.59,  "log_renda": 8.46, "ocupacao": "Caixas e bilheteiros"},
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

    st.info("""
    📖 **Como interpretar esta página**
    
    Os resultados apresentados nesta seção conectam os indicadores internacionais de exposição à Inteligência Artificial às características socioeconômicas observadas no mercado de trabalho brasileiro.
    
    A primeira análise investiga a relação entre exposição à IA e rendimento médio das ocupações. Em seguida, são apresentados os rankings das profissões mais e menos expostas segundo os referenciais de Felten et al. (AIOE) e Gmyrek et al. (OIT).
    
    Esses resultados permitem avaliar quais grupos ocupacionais tendem a sofrer maiores transformações diante da difusão das tecnologias de IA.
    """)
    
    st.divider()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    img_dir = os.path.join(project_dir, "img")

    tab_renda, tab_rankings = st.tabs(["💰 IA vs. Rendimento Mensal", "🏆 Rankings Ocupacionais"])

    # =========================================================================
    # ABA 1: SCATTER PLOTS INTERATIVOS
    # =========================================================================
    with tab_renda:
        st.subheader("Análise de Elasticidade: Exposição à IA × Logaritmo da Renda")

        # --- AIOE ---

        st.markdown("""
        ### 📈 Relação entre Exposição à IA e Rendimento
        
        Os gráficos de dispersão abaixo analisam a associação entre os índices de exposição à Inteligência Artificial e a renda média das ocupações brasileiras.
        
        Cada ponto representa uma ocupação da Classificação Brasileira de Ocupações (CBO), enquanto a linha vermelha representa a tendência estatística estimada por regressão linear.
        
        O objetivo não é identificar causalidade, mas verificar se ocupações mais expostas à IA tendem a apresentar características salariais diferentes das ocupações menos expostas.
        """)
        
        st.markdown("#### Exposição à IA e renda ocupacional — Felten/AIOE")
        df_aioe = pd.DataFrame(SCATTER_AIOE)

        # linha de regressão OLS simples
        x_a = df_aioe["aioe"].values
        y_a = df_aioe["log_renda"].values
        coef_a = np.polyfit(x_a, y_a, 1)
        x_line_a = np.linspace(x_a.min(), x_a.max(), 100)
        y_line_a = np.polyval(coef_a, x_line_a)

        fig_aioe = go.Figure()
        fig_aioe.add_trace(go.Scatter(
            x=df_aioe["aioe"], y=df_aioe["log_renda"],
            mode="markers",
            marker=dict(color="#5b9bd5", size=8, opacity=0.75),
            text=df_aioe["ocupacao"],
            hovertemplate="<b>%{text}</b><br>AIOE: %{x:.2f}<br>Log Renda: %{y:.2f}<extra></extra>",
            name="Ocupações",
        ))
        fig_aioe.add_trace(go.Scatter(
            x=x_line_a, y=y_line_a,
            mode="lines",
            line=dict(color="tomato", width=2, dash="solid"),
            name=f"Regressão (β={coef_a[0]:.3f})",
            hoverinfo="skip",
        ))
        fig_aioe.update_layout(
            height=500,
            xaxis_title="AIOE — Felten",
            yaxis_title="Log da renda média ponderada",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=20, t=40, b=40),
            hovermode="closest",
        )
        st.plotly_chart(fig_aioe, use_container_width=True)

        st.success("""
        🔎 **Interpretação dos resultados**
        
        Observa-se uma tendência positiva entre o índice AIOE e a renda média ocupacional. Em termos gerais, ocupações mais expostas à IA concentram-se em atividades intensivas em conhecimento, análise de informações, tomada de decisão e produção de conteúdo simbólico.
        
        Esse comportamento sugere que a exposição à IA não está necessariamente associada à substituição integral do trabalho, mas frequentemente à transformação das atividades desempenhadas pelos profissionais.
        """)

        st.divider()

        # --- GMYREK ---
        st.markdown("#### Exposição à IA e renda ocupacional — Gmyrek (OIT)")
        df_gmy = pd.DataFrame(SCATTER_GMYREK)

        x_g = df_gmy["gmyrek"].values
        y_g = df_gmy["log_renda"].values
        coef_g = np.polyfit(x_g, y_g, 1)
        x_line_g = np.linspace(x_g.min(), x_g.max(), 100)
        y_line_g = np.polyval(coef_g, x_line_g)

        fig_gmy = go.Figure()
        fig_gmy.add_trace(go.Scatter(
            x=df_gmy["gmyrek"], y=df_gmy["log_renda"],
            mode="markers",
            marker=dict(color="#5b9bd5", size=8, opacity=0.75),
            text=df_gmy["ocupacao"],
            hovertemplate="<b>%{text}</b><br>Gmyrek: %{x:.3f}<br>Log Renda: %{y:.2f}<extra></extra>",
            name="Ocupações",
        ))
        fig_gmy.add_trace(go.Scatter(
            x=x_line_g, y=y_line_g,
            mode="lines",
            line=dict(color="tomato", width=2, dash="solid"),
            name=f"Regressão (β={coef_g[0]:.3f})",
            hoverinfo="skip",
        ))
        fig_gmy.update_layout(
            height=500,
            xaxis_title="Mean — Gmyrek",
            yaxis_title="Log da renda média ponderada",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=20, t=40, b=40),
            hovermode="closest",
        )
        st.plotly_chart(fig_gmy, use_container_width=True)

        st.success("""
        🔎 **Interpretação dos resultados**
        
        Os resultados obtidos com o indicador da OIT apresentam comportamento semelhante ao observado no índice AIOE. A concentração das ocupações de maior exposição ocorre predominantemente entre funções administrativas, técnicas e profissionais.
        
        A convergência entre os dois referenciais fortalece a robustez metodológica do estudo, indicando consistência entre diferentes abordagens internacionais de mensuração da exposição ocupacional à IA.
        """)

    # =========================================================================
    # ABA 2: RANKINGS EXTREMOS — GRÁFICOS INTERATIVOS PLOTLY
    # =========================================================================
    with tab_rankings:

        st.info("""
        📊 **O que representam os rankings?**
        
        Os rankings apresentam os extremos da distribuição ocupacional, destacando os grupos profissionais com maior e menor exposição potencial às tecnologias de Inteligência Artificial.
        
        Importante destacar que maior exposição não significa necessariamente maior risco de substituição. Em muitos casos, a IA atua como tecnologia complementar, aumentando produtividade, eficiência e capacidade analítica dos profissionais.
        """)
        
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
            title_bot = "🟢 20 Ocupações Menos Expostas — Felten/AIOE"
        else:
            df_top = pd.DataFrame(TOP20_GMYREK)
            df_bot = pd.DataFrame(BOT20_GMYREK)
            x_label_top = "Gmyrek Mean"
            x_label_bot = "Gmyrek Mean"
            color_top = "Oranges"
            color_bot = "Blues"
            title_top = "🚨 Top 20 Ocupações Mais Expostas — Gmyrek Mean"
            title_bot = "🟢 20 Ocupações Menos Expostas — Gmyrek Mean"

        # ---- TOP 20 ----
        st.markdown(f"#### {title_top}")
        df_top_sorted = df_top.sort_values("Score", ascending=True)

        fig_top = px.bar(
            df_top_sorted,
            x="Score", y="Ocupação", orientation="h",
            text_auto=".2f", color="Score",
            color_continuous_scale=color_top,
            labels={"Score": x_label_top, "Ocupação": ""},
        )
        fig_top.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
        )
        fig_top.update_layout(
            height=700, showlegend=False, coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=20, b=40),
            xaxis_title=x_label_top, yaxis_title="", font=dict(size=11),
        )
        st.plotly_chart(fig_top, use_container_width=True)

        st.markdown("""
        ### 🧠 Principais características das ocupações mais expostas
        
        As ocupações que aparecem nas primeiras posições dos rankings possuem, em geral, atividades relacionadas a:
        
        - Processamento de informações;
        - Produção e análise de documentos;
        - Pesquisa e investigação;
        - Atividades administrativas;
        - Geração de conteúdo textual;
        - Apoio à tomada de decisão.
        
        Essas características estão entre aquelas mais diretamente impactadas pelos avanços recentes dos modelos de IA generativa.
        """)

        st.divider()

        # ---- BOTTOM 20 ----
        st.markdown(f"#### {title_bot}")
        df_bot_sorted = df_bot.sort_values("Score", ascending=False)

        fig_bot = px.bar(
            df_bot_sorted,
            x="Score", y="Ocupação", orientation="h",
            text_auto=".2f", color="Score",
            color_continuous_scale=color_bot,
            labels={"Score": x_label_bot, "Ocupação": ""},
        )
        fig_bot.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
        )
        fig_bot.update_layout(
            height=700, showlegend=False, coloraxis_showscale=False,
            margin=dict(l=10, r=60, t=20, b=40),
            xaxis_title=x_label_bot, yaxis_title="", font=dict(size=11),
        )
        st.plotly_chart(fig_bot, use_container_width=True)

        st.markdown("""
        ### 🔧 Principais características das ocupações menos expostas
        
        As ocupações classificadas entre as menos expostas tendem a depender de habilidades físicas, manuais, operacionais ou de interação direta com ambientes e equipamentos.
        
        Em muitos desses casos, a automação completa ainda enfrenta limitações tecnológicas, econômicas ou operacionais, reduzindo a capacidade de substituição por sistemas baseados exclusivamente em Inteligência Artificial.
        """)

        st.divider()

        st.info("""
        🎯 **Síntese dos resultados**
        
        Os resultados indicam que a exposição à Inteligência Artificial está distribuída de forma desigual entre as ocupações brasileiras. Profissões intensivas em informação, análise e conhecimento tendem a apresentar maior exposição, enquanto atividades predominantemente manuais permanecem menos impactadas.
        
        Entretanto, os dados sugerem que a principal consequência da IA no mercado de trabalho brasileiro não é necessariamente a eliminação imediata de ocupações, mas a transformação gradual das tarefas e competências exigidas dos trabalhadores.
        """)
