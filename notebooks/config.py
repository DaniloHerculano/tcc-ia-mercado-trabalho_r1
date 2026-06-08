"""
Configuração de caminhos para rodar o projeto a partir do GitHub.

Estrutura esperada:
tcc-ia-mercado-trabalho_r1/
├── apendices/
│   ├── planilhas/
│   └── parquet/
├── notebooks/
├── src/
└── resultados/

Observação:
- Não coloque caminhos do Google Drive aqui.
- O código usa caminhos relativos ao repositório.
"""

from pathlib import Path

# Se estiver rodando a partir de notebooks/, o ROOT sobe um nível.
# Se estiver rodando a partir da raiz do repo, ajuste manualmente para Path(".")
ROOT_DIR = Path("..").resolve()

PLANILHAS_DIR = ROOT_DIR / "apendices" / "planilhas"
PARQUET_DIR = ROOT_DIR / "apendices" / "parquet"
RESULTADOS_DIR = ROOT_DIR / "resultados"

RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

# Arquivos principais
ARQUIVO_BASE_OCUPACIONAL = PLANILHAS_DIR / "cbo_final_com_felten_gmyrek_cod_FINAL_com_fuzzy.xlsx"
ARQUIVO_FUZZY = PLANILHAS_DIR / "cbo_final_fuzzy_felten.xlsx"
ARQUIVO_EMBEDDING = PLANILHAS_DIR / "embedding_residual_openai_review_classificado.xlsx"

PNAD_ANALITICA = PARQUET_DIR / "pnad_2020_2025_analitica_ia.parquet"
PNAD_FELTEN = PARQUET_DIR / "pnad_2020_2025_felten.parquet"
PNAD_GMYREK = PARQUET_DIR / "pnad_2020_2025_gmyrek.parquet"
AGREGADO_FELTEN = PARQUET_DIR / "agregado_felten_cod_ano.parquet"
AGREGADO_GMYREK = PARQUET_DIR / "agregado_gmyrek_cod_ano.parquet"

ARQUIVOS_OBRIGATORIOS = [
    ARQUIVO_BASE_OCUPACIONAL,
    ARQUIVO_FUZZY,
    ARQUIVO_EMBEDDING,
    PNAD_ANALITICA,
    PNAD_FELTEN,
    PNAD_GMYREK,
    AGREGADO_FELTEN,
    AGREGADO_GMYREK,
]
