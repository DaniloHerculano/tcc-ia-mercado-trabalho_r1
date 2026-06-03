import streamlit as st

from carregar_dados import (
    criar_base_final
)

from views.dashboard_home import mostrar_dashboard
from views.exposicao_brasil import mostrar_exposicao_brasil
from views.evolucao_temporal import mostrar_evolucao_temporal
from views.escolaridade import mostrar_escolaridade
from views.renda import mostrar_renda
from views.setores import mostrar_setores
from views.ranking import mostrar_ranking
from views.similaridade import mostrar_similaridade
from views.correlacao import mostrar_correlacao
from views.insights import mostrar_insights
from views.pesquisa import mostrar_pesquisa
from views.simulador import mostrar_simulador
from views.analise_exploratoria import mostrar_analise_exploratoria
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

    return criar_base_final()

# ==========================================
# LOAD
# ==========================================

with st.spinner("Carregando dados..."):

    df = carregar()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Navegação")

pagina = st.sidebar.radio(
    "Selecione:",
    [
        # "📊 Dashboard",
        "🔗 Analise Exploratoria",
        "🇧🇷 Exposição no Brasil",
        "📈 Evolução Temporal",
        # "🎓 Escolaridade x IA",
        # "💰 Renda x IA",
        "🏭 Mapa Exposição a IA",
        # "🏆 Ranking",
        # "🔥 Correlação",
        # "🧠 Insights IA",
        "🪞 Similaridade",
        # "🔎 Pesquisar Ocupação",
        "🤖 Simulador IA",
        "ℹ️ Sobre"
    ]
)

st.sidebar.divider()

# ==========================================
# ROTAS
# ==========================================

if pagina == "📊 Dashboard":

    mostrar_dashboard(df)

elif pagina == "🇧🇷 Exposição no Brasil":

    mostrar_exposicao_brasil(df)

elif pagina == "📈 Evolução Temporal":

    mostrar_evolucao_temporal(df)

elif pagina == "🔗 Analise Exploratoria":

    mostrar_analise_exploratoria(df)

elif pagina == "🎓 Escolaridade x IA":

    mostrar_escolaridade(df)

elif pagina == "💰 Renda x IA":

    mostrar_renda(df)

elif pagina == "🏭 Mapa Exposição a IA":

    mostrar_setores(df)

elif pagina == "🏆 Ranking":

    mostrar_ranking(df)

elif pagina == "🔥 Correlação":

    mostrar_correlacao(df)

elif pagina == "🧠 Insights IA":

    mostrar_insights(df)

elif pagina == "🪞 Similaridade":

    mostrar_similaridade(df)

elif pagina == "🔎 Pesquisar Ocupação":

    mostrar_pesquisa(df)

elif pagina == "🤖 Simulador IA":

    mostrar_simulador(df)

elif pagina == "ℹ️ Sobre":

    mostrar_sobre()
