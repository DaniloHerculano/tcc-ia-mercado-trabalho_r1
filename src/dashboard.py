import streamlit as st

from carregar_dados import (
    carregar_cbo,
    carregar_pnad,
    limpar_dados
)

from views.dashboard_home import mostrar_dashboard
from views.impacto_brasil import mostrar_impacto_brasil
from views.evolucao_temporal import mostrar_evolucao_temporal
from views.escolaridade import mostrar_escolaridade
from views.renda import mostrar_renda
from views.setores import mostrar_setores
from views.ranking import mostrar_ranking
from views.similaridade import mostrar_similaridade
from views.pesquisa import mostrar_pesquisa
from views.sobre import mostrar_sobre

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IA e Mercado de Trabalho",
    layout="wide"
)

# ==========================================
# CACHE
# ==========================================

@st.cache_data
def carregar():

    df = carregar_cbo()
    df = limpar_dados(df)

    df_pnad = carregar_pnad()

    return df, df_pnad

# ==========================================
# LOADING
# ==========================================

with st.spinner("Carregando dados..."):

    df, df_pnad = carregar()

# ==========================================
# MENU
# ==========================================

st.sidebar.title("📌 Navegação")

pagina = st.sidebar.radio(
    "Selecione:",
    [
        "📊 Dashboard",
        "🇧🇷 Impacto no Brasil",
        "📈 Evolução Temporal",
        "🎓 Escolaridade x IA",
        "💰 Renda x IA",
        "🏭 Setores x IA",
        "🏆 Ranking",
        "🧠 Similaridade",
        "🔎 Pesquisar Ocupação",
        "ℹ️ Sobre"
    ]
)

# ==========================================
# ROTAS
# ==========================================

if pagina == "📊 Dashboard":
    mostrar_dashboard(df)

elif pagina == "🇧🇷 Impacto no Brasil":
    mostrar_impacto_brasil(df, df_pnad)

elif pagina == "📈 Evolução Temporal":
    mostrar_evolucao_temporal(df, df_pnad)

elif pagina == "🎓 Escolaridade x IA":
    mostrar_escolaridade(df, df_pnad)

elif pagina == "💰 Renda x IA":
    mostrar_renda(df, df_pnad)

elif pagina == "🏭 Setores x IA":
    mostrar_setores(df)

elif pagina == "🏆 Ranking":
    mostrar_ranking(df)

elif pagina == "🧠 Similaridade":
    mostrar_similaridade(df)

elif pagina == "🔎 Pesquisar Ocupação":
    mostrar_pesquisa(df)

elif pagina == "ℹ️ Sobre":
    mostrar_sobre()