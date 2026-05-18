import streamlit as st

from src.carregar_dados import (
    criar_base_final
)

from src.views.dashboard_home import mostrar_dashboard
from src.views.impacto_brasil import mostrar_impacto_brasil
from src.views.evolucao_temporal import mostrar_evolucao_temporal
from src.views.escolaridade import mostrar_escolaridade
from src.views.renda import mostrar_renda
from src.views.setores import mostrar_setores
from src.views.ranking import mostrar_ranking
from src.views.similaridade import mostrar_similaridade
from src.views.pesquisa import mostrar_pesquisa
from src.views.sobre import mostrar_sobre

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

    df = criar_base_final()

    return df

# ==========================================
# LOADING
# ==========================================

with st.spinner("Carregando dados..."):

    df = carregar()

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
    mostrar_impacto_brasil(df)

elif pagina == "📈 Evolução Temporal":
    mostrar_evolucao_temporal(df)

elif pagina == "🎓 Escolaridade x IA":
    mostrar_escolaridade(df)

elif pagina == "💰 Renda x IA":
    mostrar_renda(df)

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


# ==========================================
# CRIAR BASE FINAL
# ==========================================

def criar_base_final():

    # CARREGAR
    df_cbo = carregar_cbo()

    df_pnad = carregar_pnad()

    # LIMPAR
    df_cbo = limpar_dados(df_cbo)

    df_pnad = limpar_pnad(df_pnad)

    # CRUZAR
    df_final = cruzar_bases(
        df_cbo,
        df_pnad
    )

    return df_final