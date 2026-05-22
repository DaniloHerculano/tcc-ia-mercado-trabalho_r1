import os
import pandas as pd
import gdown

# ==========================================
# CAMINHOS
# ==========================================

ARQUIVO_CBO = (
    "data/cbo_final_com_felten_gmyrek_cod_FINAL.xlsx"
)

# ==========================================
# GOOGLE DRIVE
# ==========================================

FILE_ID = "1kfa3fXfkSMT3qAUP1OjKJCBjHFQvppOm"

URL_PNAD = (
    f"https://drive.google.com/uc?/export=download&id={FILE_ID}"
)

ARQUIVO_PNAD_LOCAL = (
    "data/pnad_2020_2025_analitica_ia.parquet"
)

# ==========================================
# DOWNLOAD PNAD
# ==========================================

def baixar_pnad():

    if os.path.exists(ARQUIVO_PNAD_LOCAL):
        return

    os.makedirs("data", exist_ok=True)

    gdown.download(
        URL_PNAD,
        ARQUIVO_PNAD_LOCAL,
        quiet=False
    )

# ==========================================
# CARREGAR CBO
# ==========================================

def carregar_cbo():

    print("\n========== DEBUG CBO ==========")

    print("Diretório atual:")
    print(os.getcwd())

    print("\nArquivos na pasta data:")

    if os.path.exists("data"):

        print(os.listdir("data"))

    else:

        print("PASTA DATA NÃO EXISTE")

    print("\nTentando abrir:")
    print(ARQUIVO_CBO)

    print("\nExiste?")
    print(os.path.exists(ARQUIVO_CBO))

    if not os.path.exists(ARQUIVO_CBO):

        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_CBO}"
        )

    df = pd.read_excel(
        ARQUIVO_CBO
    )

    print("\nCOLUNAS CBO:")
    print(df.columns.tolist())

    return df

# ==========================================
# CARREGAR PNAD
# ==========================================

def carregar_pnad():

    baixar_pnad()

    df = pd.read_parquet(
        ARQUIVO_PNAD_LOCAL
    )

    print("\nCOLUNAS PNAD:")
    print(df.columns.tolist())

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

        .str.extract(r'(\d+)')[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

    # ======================================
    # NUMÉRICOS
    # ======================================

    df["AIOE"] = pd.to_numeric(
        df["AIOE"],
        errors="coerce"
    )

    df["Exposure"] = pd.to_numeric(
        df["Exposure"],
        errors="coerce"
    )

    # ======================================
    # NÍVEL IMPACTO
    # ======================================

    def classificar(score):

        if pd.isna(score):
            return "Não informado"

        if score >= 0.75:
            return "🔴 Alto"

        elif score >= 0.45:
            return "🟡 Médio"

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

    colunas_numericas = [

        "Idade",
        "Rendimento_Mensal",
        "AIOE",
        "Exposure",
        "Mean",
        "SD"
    ]

    for col in colunas_numericas:

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

        .str.extract(r'(\d+)')[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

    # ======================================
    # SEXO
    # ======================================

    mapa_sexo = {
        "1": "Masculino",
        "2": "Feminino"
    }

    df["Sexo"] = (
        df["Sexo"]
        .astype(str)
        .replace(mapa_sexo)
    )

    return df

# ==========================================
# CRUZAR BASES
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

        "COD_Grupo_Base",
        "COD_Titulacao",

        "COD_Grande_Grupo",
        "COD_Subgrupo_principal",
        "COD_Subgrupo",

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
    # PADRONIZAÇÃO NOMES
    # ======================================

    df_final["AIOE_SCORE"] = (
        df_final["AIOE"]
    )

    df_final["AIOE_MATCH_TITLE"] = (
        df_final["ISCO-08 Title"]
        if "ISCO-08 Title" in df_final.columns
        else None
    )

    df_final["CONFIDENCE_SCORE"] = (
        df_final["Mean"]
    )

    print("\nMATCHES:")
    print(
        df_final["AIOE_SCORE"]
        .notna()
        .sum()
    )

    return df_final

# ==========================================
# BASE FINAL
# ==========================================

def criar_base_final():

    df_cbo = carregar_cbo()

    df_pnad = carregar_pnad()

    df_cbo = limpar_cbo(df_cbo)

    df_pnad = limpar_pnad(df_pnad)

    df_final = cruzar_bases(
        df_cbo,
        df_pnad
    )

    print("\nBASE FINAL:")
    print(df_final.head())

    return df_final