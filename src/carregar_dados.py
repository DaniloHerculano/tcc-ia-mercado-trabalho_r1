import pandas as pd

# ==========================================
# CAMINHOS
# ==========================================

ARQUIVO_CBO = (
    "data/tabela_cbo_aioe_filtrada_tcc.xlsx"
)

ARQUIVO_PNAD = (
    "data/pnad_completa_HISTORICO_LIMPA.parquet"
)

ARQUIVO_DICIONARIO = (
    "data/dicionario_PNADC_microdados_trimestral.xlsx"
)

# ==========================================
# CARREGAR CBO / AIOE
# ==========================================

def carregar_cbo():

    df = pd.read_excel(
        ARQUIVO_CBO
    )

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

    df = pd.read_parquet(
        ARQUIVO_PNAD,
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
    # NUMÉRICOS
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
            "TITULO_LIMPO",
            "AIOE_SCORE"
        ]
    )

    # ======================================
    # CBO JOIN
    # ======================================

    df["CBO_JOIN"] = (
        df["CBO_EXTRAIDO"]
        .astype(str)
        .str.replace("-", "")
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
    # CBO JOIN
    # ======================================

    df["CBO_JOIN"] = (
        df["CBO"]
        .astype(str)
        .str.replace("-", "")
        .str.strip()
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
    # SITUAÇÃO DOMICÍLIO
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
        "TITULO_LIMPO",
        "AIOE_SCORE",
        "NIVEL_IMPACTO",
        "FORMAÇÃO E EXPERIÊNCIA",
        "DESCRIÇÃO SUMÁRIA",
        "AIOE_MATCH_TITLE"
    ]

    df_final = pd.merge(

        df_pnad,
        df_cbo[colunas_merge],

        on="CBO_JOIN",
        how="left"
    )

    return df_final