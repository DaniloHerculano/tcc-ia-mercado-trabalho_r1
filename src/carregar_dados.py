import os
import pandas as pd

# ==========================================
# CAMINHOS
# ==========================================

ARQUIVO_CBO = (
    "data/cbo_final_com_felten_gmyrek_cod_FINAL.xlsx"
)

ARQUIVO_PNAD = (
    "data/pnad_2020_2025_analitica_ia.parquet"
)

# ==========================================
# CARREGAR CBO
# ==========================================

def carregar_cbo():

    df = pd.read_excel(
        ARQUIVO_CBO,
        engine="openpyxl"
    )

    return df

# ==========================================
# CARREGAR PNAD
# ==========================================

def carregar_pnad():

    df = pd.read_parquet(
        ARQUIVO_PNAD
    )

    return df

# ==========================================
# LIMPAR CBO
# ==========================================

def limpar_cbo(df):

    # ======================================
    # CBO JOIN
    # ======================================

    df["CBO_JOIN"] = (

        df["CBO_EXTRAIDO"]

        .astype(str)

        .str.extract(r"(\d+)")[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

    # ======================================
    # NUMÉRICOS
    # ======================================

    numeros = [
        "AIOE",
        "Exposure",
        "Mean",
        "SD"
    ]

    for col in numeros:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # ======================================
    # IMPACTO
    # ======================================

    def classificar(score):

        if pd.isna(score):
            return "Não informado"

        if score >= 0.75:
            return "🔴 Alto"

        elif score >= 0.45:
            return "🟡 Médio"

        else:
            return "🟢 Baixo"

    df["NIVEL_IMPACTO"] = (
        df["AIOE"]
        .apply(classificar)
    )

    return df

# ==========================================
# LIMPAR PNAD
# ==========================================

def limpar_pnad(df):

    # ======================================
    # NUMÉRICOS
    # ======================================

    numeros = [

        "Ano",
        "Trimestre",
        "Idade",
        "Rendimento_Mensal",
        "AIOE",
        "Exposure",
        "Mean",
        "SD"
    ]

    for col in numeros:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # ======================================
    # CBO JOIN
    # ======================================

    df["CBO_JOIN"] = (

        df["CBO"]

        .astype(str)

        .str.extract(r"(\d+)")[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

    # ======================================
    # SEXO
    # ======================================

    mapa_sexo = {

        "1": "Masculino",
        "2": "Feminino",

        1: "Masculino",
        2: "Feminino"
    }

    df["Sexo"] = (
        df["Sexo"]
        .replace(mapa_sexo)
    )

    return df

# ==========================================
# MERGE
# ==========================================

def cruzar_bases(df_cbo, df_pnad):

    colunas_merge = [

        "CBO_JOIN",

        "CBO_EXTRAIDO",
        "TITULO_LIMPO",

        "DESCRIÇÃO SUMÁRIA",
        "FORMAÇÃO E EXPERIÊNCIA",

        "AIOE",
        "Exposure",
        "Mean",
        "SD",

        "NIVEL_IMPACTO",

        "COD_Grande_Grupo_TITULO",
        "COD_Subgrupo_principal_TITULO",
        "COD_Subgrupo_TITULO",

        "match_cod_metodo"
    ]

    df_final = pd.merge(

        df_pnad,

        df_cbo[colunas_merge],

        on="CBO_JOIN",

        how="left"
    )

    # ======================================
    # PADRONIZAÇÃO
    # ======================================

    df_final["AIOE_SCORE"] = (
        df_final["AIOE_y"]
        if "AIOE_y" in df_final.columns
        else df_final["AIOE"]
    )

    df_final["CONFIDENCE_SCORE"] = (
        df_final["Mean_y"]
        if "Mean_y" in df_final.columns
        else df_final["Mean"]
    )

    df_final["Grande Grupo"] = (
        df_final["COD_Grande_Grupo_TITULO"]
    )

    df_final["Subgrupo"] = (
        df_final["COD_Subgrupo_TITULO"]
    )

    df_final["AIOE_MATCH_TITLE"] = (
        df_final["match_cod_metodo"]
    )

    return df_final

# ==========================================
# BASE FINAL
# ==========================================

def criar_base_final():

    # ======================================
    # CARREGAR
    # ======================================

    df_cbo = carregar_cbo()

    df_pnad = carregar_pnad()

    # ======================================
    # LIMPAR
    # ======================================

    df_cbo = limpar_cbo(df_cbo)

    df_pnad = limpar_pnad(df_pnad)

    # ======================================
    # MERGE
    # ======================================

    df_final = cruzar_bases(
        df_cbo,
        df_pnad
    )

    print("\nBASE FINAL:")
    print(df_final.head())

    return df_final