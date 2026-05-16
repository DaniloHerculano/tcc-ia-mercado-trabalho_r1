import pandas as pd


# ==========================================
# CARREGAR BASE CBO
# ==========================================

def carregar_cbo():

    caminho = (
        "data/tabela_cbo_e5_large_final.xlsx"
    )

    df = pd.read_excel(caminho)

    return df


# ==========================================
# CARREGAR PNAD
# ==========================================

def carregar_pnad():

    df = pd.read_parquet(
        "data/pnad_processada.parquet"
    )

    return df

# ==========================================
# LIMPEZA BASE CBO
# ==========================================

def limpar_dados(df):

    # ======================================
    # REMOVER NULOS IMPORTANTES
    # ======================================

    df = df.dropna(
        subset=[
            "TITULO_LIMPO",
            "AIOE_SCORE"
        ]
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
            "AIOE_SCORE",
            "CONFIDENCE_SCORE"
        ]
    )

    # ======================================
    # NÍVEL IMPACTO
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


# ==========================================
# LIMPEZA PNAD
# ==========================================

def limpar_pnad(df):

    # ======================================
    # CONVERTER TIPOS
    # ======================================

    df["Ano"] = (
        pd.to_numeric(
            df["Ano"],
            errors="coerce"
        )
    )

    df["Idade"] = (
        pd.to_numeric(
            df["Idade"],
            errors="coerce"
        )
    )

    df["Rendimento_Mensal"] = (
        pd.to_numeric(
            df["Rendimento_Mensal"],
            errors="coerce"
        )
    )

    # ======================================
    # REMOVER NULOS
    # ======================================

    df = df.dropna(
        subset=[
            "Ano",
            "UF",
            "Sexo",
            "Idade"
        ]
    )

    return df