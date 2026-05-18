import pandas as pd

df = pd.read_parquet(
    "data/pnad_completa_HISTORICO_LIMPA.parquet"
)

df.to_csv(
    "data/pnad.csv",
    index=False
)