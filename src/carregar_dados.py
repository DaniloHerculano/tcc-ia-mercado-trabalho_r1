import pandas as pd


# ==========================================
# CARREGAR BASE PRINCIPAL
# ==========================================

def carregar_cbo():

    caminho = (
        "data/"
        "tabela_cbo_e5_large_final.xlsx"
    )

    df = pd.read_excel(caminho)

    return df


# ==========================================
# LIMPEZA
# ==========================================

def limpar_dados(df):

    df = df.copy()

    # ======================================
    # REMOVER NULOS
    # ======================================

    df = df.dropna(
        subset=[
            "AIOE_SCORE",
            "CONFIDENCE_SCORE"
        ]
    )

    # ======================================
    # CONVERTER SCORES
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
    # CRIAR NÍVEL DE IMPACTO
    # ======================================

    def classificar(score):

        if score >= 0.75:
            return "🔴 Alto"

        elif score >= 0.45:
            return "🟡 Médio"

        else:
            return "🟢 Baixo"

    df["NIVEL_IMPACTO"] = (
        df["AIOE_SCORE"]
        .apply(classificar)
    )

    return df