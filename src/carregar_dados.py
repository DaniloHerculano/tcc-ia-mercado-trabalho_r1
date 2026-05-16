# ==========================================
# src/carregar_dados.py
# ==========================================

import pandas as pd


# ==========================================
# CLASSIFICAÇÃO DE IMPACTO
# ==========================================

def classificar_impacto(score):

    if score >= 0.70:
        return "🔴 Alto"

    elif score >= 0.40:
        return "🟡 Médio"

    else:
        return "🟢 Baixo"


# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_dados():

    caminho = (
        "data/tabela_cbo_e5_large_final.xlsx"
    )

    df = pd.read_excel(caminho)

    # ======================================
    # LIMPEZA
    # ======================================

    df.columns = (
        df.columns
        .str.strip()
    )

    # ======================================
    # TEXTO
    # ======================================

    colunas_texto = [
        "TITULO_LIMPO",
        "Grande Grupo",
        "AIOE_MATCH_TITLE"
    ]

    for coluna in colunas_texto:

        if coluna in df.columns:

            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.strip()
            )

    # ======================================
    # NUMÉRICOS
    # ======================================

    df["AIOE_SCORE"] = pd.to_numeric(
        df["AIOE_SCORE"],
        errors="coerce"
    )

    df["CONFIDENCE_SCORE"] = pd.to_numeric(
        df["CONFIDENCE_SCORE"],
        errors="coerce"
    )

    # ======================================
    # REMOVER NULOS
    # ======================================

    df = df.dropna(
        subset=[
            "TITULO_LIMPO",
            "AIOE_SCORE",
            "CONFIDENCE_SCORE"
        ]
    )

    # ======================================
    # CLASSIFICAÇÃO
    # ======================================

    df["NIVEL_IMPACTO"] = (
        df["AIOE_SCORE"]
        .apply(classificar_impacto)
    )

    return df