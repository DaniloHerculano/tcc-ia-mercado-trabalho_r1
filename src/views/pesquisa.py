import streamlit as st


# ==========================================
# PESQUISA
# ==========================================

def mostrar_pesquisa(df):

    st.title(
        "🔎 Pesquisa de Ocupações"
    )

    st.markdown("""
    Consulte ocupações brasileiras
    e visualize o nível de exposição
    à Inteligência Artificial.
    """)

    st.divider()

    # ======================================
    # BUSCA
    # ======================================

    busca = st.text_input(
        "Digite uma ocupação"
    )

    # ======================================
    # FILTRO IMPACTO
    # ======================================

    filtro = st.selectbox(
        "Filtrar impacto",
        [
            "Todos",
            "🔴 Alto",
            "🟡 Médio",
            "🟢 Baixo"
        ]
    )

    # ======================================
    # FILTRO GRUPO
    # ======================================

    grupos = sorted(
        df["Grande Grupo"]
        .dropna()
        .unique()
        .tolist()
    )

    grupo = st.selectbox(
        "Grande Grupo",
        ["Todos"] + grupos
    )

    # ======================================
    # FILTROS
    # ======================================

    resultado = df.copy()

    if filtro != "Todos":

        resultado = resultado[
            resultado["NIVEL_IMPACTO"]
            == filtro
        ]

    if grupo != "Todos":

        resultado = resultado[
            resultado["Grande Grupo"]
            == grupo
        ]

    if busca:

        resultado = resultado[
            resultado["TITULO_LIMPO"]
            .astype(str)
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    st.divider()

    st.info(
        f"{len(resultado)} ocupações encontradas."
    )

    # ======================================
    # RESULTADOS
    # ======================================

    for _, row in resultado.head(30).iterrows():

        st.markdown(f"""
        ---
        ## {row['TITULO_LIMPO']}

        **CBO:** {row['CBO_EXTRAIDO']}

        **Impacto IA:** {row['NIVEL_IMPACTO']}

        **AIOE Score:** {round(row['AIOE_SCORE'], 3)}

        **Confiança:** {round(row['CONFIDENCE_SCORE'], 3)}

        **Match AIOE:** {row['AIOE_MATCH_TITLE']}

        **Grande Grupo:** {row['Grande Grupo']}

        **Subgrupo:** {row['Subgrupo']}
        """)

        with st.expander(
            "Ver descrição"
        ):

            st.write(
                row[
                    "DESCRIÇÃO SUMÁRIA"
                ]
            )