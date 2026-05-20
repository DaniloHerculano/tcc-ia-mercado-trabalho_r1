import os
import pandas as pd
import gdown

# ==========================================
# CAMINHOS
# ==========================================

ARQUIVO_CBO = (
    "data/tabela_cbo_aioe_filtrada_tcc.xlsx"
)

ARQUIVO_DICIONARIO = (
    "data/dicionario_PNADC_microdados_trimestral.xlsx"
)

# ==========================================
# GOOGLE DRIVE
# ==========================================

FILE_ID = "1lYFw5ruJAhvHnVpQWgJVYTHePtONS32V"

URL_PNAD = (
    f"https://drive.google.com/uc?/export=download&id={FILE_ID}"
)

ARQUIVO_PNAD_LOCAL = (
    "data/pnad_completa_HISTORICO_LIMPA.parquet"
)

# ==========================================
# DOWNLOAD PNAD
# ==========================================

def baixar_pnad():

    # ======================================
    # SE JÁ EXISTE
    # ======================================

    if os.path.exists(ARQUIVO_PNAD_LOCAL):
        return

    # ======================================
    # CRIAR PASTA
    # ======================================

    os.makedirs("data", exist_ok=True)

    # ======================================
    # DOWNLOAD GOOGLE DRIVE
    # ======================================

    gdown.download(
        URL_PNAD,
        ARQUIVO_PNAD_LOCAL,
        quiet=False
    )

# ==========================================
# CARREGAR CBO / AIOE
# ==========================================

def carregar_cbo():

    df = pd.read_excel(
        ARQUIVO_CBO
    )

    print(df.columns.tolist())

    return df

# ==========================================
# CARREGAR PNAD
# ==========================================

def carregar_pnad():

    colunas = [
        "Ano",
        "Trimestre",
        "UF",
        "Situacao_Domicilio",
        "Sexo",
        "Idade",
        "CBO",
        "Anos_Estudo",
        "Rendimento_Mensal"
    ]

    # ======================================
    # BAIXAR SE NÃO EXISTIR
    # ======================================

    baixar_pnad()

    # ======================================
    # LER PARQUET
    # ======================================

    df = pd.read_parquet(
        ARQUIVO_PNAD_LOCAL,
        columns=colunas
    )

    # ======================================
    # REDUZIR AMOSTRA
    # ======================================

    if len(df) > 300000:

        df = df.sample(
            n=300000,
            random_state=42
        )

    return df

# ==========================================
# LIMPAR CBO
# ==========================================

def limpar_dados(df):

    # ======================================
    # RENOMEAR
    # ======================================

    df = df.rename(columns={

        "AIOE_score": "AIOE_SCORE",

        "Occupation_Title_AIOE":
        "AIOE_MATCH_TITLE"

    })

    # ======================================
    # NUMÉRICO
    # ======================================

    df["AIOE_SCORE"] = pd.to_numeric(
        df["AIOE_SCORE"],
        errors="coerce"
    )

    # ======================================
    # REMOVER NULOS
    # ======================================

    df = df.dropna(
        subset=[
            "CBO_EXTRAIDO",
            "AIOE_SCORE"
        ]
    )

    # ======================================
    # AJUSTAR CBO
    # ======================================

    df["CBO_JOIN"] = (

        df["CBO"]

        .astype(str)

        .str.replace(r"\D", "", regex=True)

        .str.strip()

        .str.zfill(6)
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

    # ======================================
    # CAMPOS AUXILIARES
    # ======================================

    df["CONFIDENCE_SCORE"] = 1.0

    df["Grande Grupo"] = (
        df["CBO_JOIN"]
        .str[0]
    )

    # ======================================
    # DEBUG
    # ======================================

    print("\nCBO LIMPO:")
    print(
        df[
            [
                "CBO_EXTRAIDO",
                "CBO_JOIN",
                "TITULO_LIMPO",
                "AIOE_SCORE"
            ]
        ].head(20)
    )

    return df

# ==========================================
# LIMPAR PNAD
# ==========================================

def limpar_pnad(df):

    # ======================================
    # NUMÉRICOS
    # ======================================

    df["Ano"] = pd.to_numeric(
        df["Ano"],
        errors="coerce"
    )

    df["Idade"] = pd.to_numeric(
        df["Idade"],
        errors="coerce"
    )

    df["Rendimento_Mensal"] = (
        pd.to_numeric(
            df["Rendimento_Mensal"],
            errors="coerce"
        )
    )

    # ======================================
    # AJUSTAR CBO
    # ======================================

    df["CBO_JOIN"] = (

        df["CBO"]

        .astype(str)

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

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
        .map(mapa_sexo)
    )

    # ======================================
    # DOMICÍLIO
    # ======================================

    mapa_dom = {
        "1": "Urbana",
        "2": "Rural"
    }

    df["Situacao_Domicilio"] = (
        df["Situacao_Domicilio"]
        .astype(str)
        .map(mapa_dom)
    )

    return df

# ==========================================
# MERGE PNAD + AIOE
# ==========================================

def cruzar_bases(df_cbo, df_pnad):

    colunas_merge = [

        "CBO_JOIN",
        "CBO_EXTRAIDO",
        "TITULO_LIMPO",
        "DESCRIÇÃO SUMÁRIA",
        "FORMAÇÃO E EXPERIÊNCIA",
        "AIOE_SCORE",
        "AIOE_MATCH_TITLE",
        "NIVEL_IMPACTO",
        "CONFIDENCE_SCORE",
        "Grande Grupo"
    ]

    df_final = pd.merge(

        df_pnad,

        df_cbo[colunas_merge],

        on="CBO_JOIN",

        how="left"
    )

    print("\nMERGE RESULTADO:")
    print(
        df_final[
            [
                "CBO",
                "CBO_JOIN",
                "CBO_EXTRAIDO",
                "TITULO_LIMPO",
                "AIOE_SCORE"
            ]
        ].head(30)
    )

    return df_final

# ==========================================
# CRIAR BASE FINAL
# ==========================================

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

    print(df_final.columns.tolist())

    print(df_final[
        [
            "CBO",
            "CBO_JOIN",
            "CBO_EXTRAIDO",
            "TITULO_LIMPO",
            "AIOE_SCORE"
        ]
    ].head(20))

    return df_final