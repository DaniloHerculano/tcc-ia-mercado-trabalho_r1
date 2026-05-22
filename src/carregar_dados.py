```python
import pandas as pd

# ==========================================
# CAMINHOS
# ==========================================

ARQUIVO_CBO = (
    "data/cbo_final_com_felten_gmyrek_cod_FINAL.xlsx"
)

ARQUIVO_PNAD_LOCAL = (
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

    print("\nCOLUNAS CBO:")
    print(df.columns.tolist())

    return df

# ==========================================
# CARREGAR PNAD
# ==========================================

def carregar_pnad():

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

    df["CBO_JOIN"] = (

        df["CBO_EXTRAIDO"]

        .astype(str)

        .str.extract(r"(\d+)")[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

    df["AIOE"] = pd.to_numeric(
        df["AIOE"],
        errors="coerce"
    )

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

    numeros = [

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

    df["CBO_JOIN"] = (

        df["CBO"]

        .astype(str)

        .str.extract(r"(\d+)")[0]

        .str.replace(r"\D", "", regex=True)

        .str.zfill(6)

        .str[:6]
    )

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
# MERGE
# ==========================================

def cruzar_bases(df_cbo, df_pnad):

    colunas = [

        "CBO_JOIN",
        "CBO_EXTRAIDO",
        "TITULO_LIMPO",
        "DESCRIÇÃO SUMÁRIA",

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

        df_cbo[colunas],

        on="CBO_JOIN",

        how="left"
    )

    df_final["AIOE_SCORE"] = (
        df_final["AIOE"]
    )

    df_final["CONFIDENCE_SCORE"] = (
        df_final["Mean"]
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

    print("\nBASE FINAL:")
    print(df_final.head())

    return df_final

# ==========================================
# FINAL
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

    return df_final