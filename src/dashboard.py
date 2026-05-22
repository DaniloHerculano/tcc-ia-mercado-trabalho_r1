import streamlit as st

from carregar_dados import criar_base_final

from views.dashboard_home import mostrar_dashboard

st.set_page_config(
    page_title="IA e Mercado",
    layout="wide"
)

st.title("TESTE VIEW")

@st.cache_data
def carregar():

    return criar_base_final()

df = carregar()

st.success("Dados carregados!")

try:

    mostrar_dashboard(df)

except Exception as e:

    st.error("Erro na view dashboard_home")
    st.exception(e)