# ==========================================
# FILTRO IMPACTO
# ==========================================

def filtrar_impacto(
    df,
    impacto
):

    if impacto == "Todos":

        return df

    return df[
        df["NIVEL_IMPACTO"]
        == impacto
    ]


# ==========================================
# FILTRO TEXTO
# ==========================================

def filtrar_texto(
    df,
    coluna,
    texto
):

    if not texto:

        return df

    return df[
        df[coluna]
        .astype(str)
        .str.contains(
            texto,
            case=False,
            na=False
        )
    ]