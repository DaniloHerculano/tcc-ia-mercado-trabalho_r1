import streamlit as st

from carregar_dados import (
    carregar_cbo,
    carregar_pnad,
    limpar_dados,
    limpar_pnad
)

# ==========================================
# IMPORTAR PÁGINAS
# ==========================================

from pages.dashboard_home import (
    mostrar_dashboard
)

from pages.impacto_brasil import (
    mostrar_impacto_brasil
)

from pages.evolucao_temporal import (
    mostrar_evolucao_temporal
)

from pages.escolaridade import (
    mostrar_escolaridade
)

from pages.renda import (
    mostrar_renda
)

from pages.setores import (
    mostrar_setores
)

from pages.ranking import (
    mostrar_ranking
)

from pages.similaridade import (
    mostrar_similaridade
)

from pages.pesquisa import (
    mostrar_pesquisa
)

from pages.sobre import (
    mostrar_sobre
)

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="IA e Mercado de Trabalho",
    layout="wide"
)

# ==========================================
# CARREGAR DADOS
# ==========================================

@st.cache_data
def carregar_bases():

    # ======================================
    # CBO
    # ======================================

    df_cbo = carregar_cbo()

    df_cbo = limpar_dados(df_cbo)

    # ======================================
    # PNAD
    # ======================================

    df_pnad = carregar_pnad()

    df_pnad = limpar_pnad(df_pnad)

    return df_cbo, df_pnad


df, df_pnad = carregar_bases()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title(
    "📌 Navegação"
)

pagina = st.sidebar.radio(
    "Selecione:",
    [
        "📊 Dashboard",
        "🇧🇷 Impacto no Brasil",
        "📅 Evolução Temporal",
        "🎓 Escolaridade x IA",
        "💰 Renda x IA",
        "🏭 Setores x IA",
        "🔎 Pesquisar Ocupação",
        "🏆 Ranking",
        "🧠 Similaridade",
        "ℹ️ Sobre"
    ]
)

# ==========================================
# ROTAS
# ==========================================

if pagina == "📊 Dashboard":

    mostrar_dashboard(df)

elif pagina == "🇧🇷 Impacto no Brasil":

    mostrar_impacto_brasil(
        df,
        df_pnad
    )

elif pagina == "📅 Evolução Temporal":

    mostrar_evolucao_temporal(
        df_pnad
    )

elif pagina == "🎓 Escolaridade x IA":

    mostrar_escolaridade(df)

elif pagina == "💰 Renda x IA":

    mostrar_renda(df_pnad)

elif pagina == "🏭 Setores x IA":

    mostrar_setores(df)

elif pagina == "🔎 Pesquisar Ocupação":

    mostrar_pesquisa(df)

elif pagina == "🏆 Ranking":

    mostrar_ranking(df)

elif pagina == "🧠 Similaridade":

    mostrar_similaridade(df)

elif pagina == "ℹ️ Sobre":

    mostrar_sobre()