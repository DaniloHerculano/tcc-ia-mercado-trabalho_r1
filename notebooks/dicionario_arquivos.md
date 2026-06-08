# Dicionário de Arquivos

Este documento descreve os principais arquivos finais utilizados para documentar e reproduzir as análises do TCC.

## Planilhas

### `cbo_final_com_felten_gmyrek_cod_FINAL_com_fuzzy.xlsx`

Base ocupacional final contendo a integração entre:

- CBO;
- COD;
- ISCO-88;
- ISCO-08;
- SOC 2010;
- AIOE;
- Exposure;
- Mean;
- SD;
- resultados do fuzzy matching.

Esta é a principal tabela ocupacional final do projeto.

### `cbo_final_fuzzy_felten.xlsx`

Tabela com os resultados do fuzzy matching aplicado às ocupações remanescentes sem score AIOE após os métodos estruturais de compatibilização.

### `embedding_residual_openai_review_classificado.xlsx`

Tabela de revisão dos embeddings semânticos utilizados para casos residuais. Esses resultados não foram incorporados automaticamente à base final.

### `AIOE_DataAltered.xlsx`

Tabela derivada do trabalho de Felten et al. (2021), contendo os scores AIOE utilizados no processo de herança ocupacional.

### `gymrek_2025_scores.xlsx`

Tabela derivada do trabalho de Gmyrek et al. (2025), contendo os indicadores `Exposure`, `Mean` e `SD`.

### `Correspondence_EN_ISCO_88_to_ISCO_08-altered.xlsx`

Tabela de correspondência entre ISCO-88 e ISCO-08.

### `isco_soc_crosswalk_altered.xlsx`

Tabela de correspondência entre ISCO-08 e SOC 2010.

### `soc_2010_definitions.xls`

Tabela com códigos, títulos e definições ocupacionais da SOC 2010.

## Parquets

### `pnad_2020_2025_analitica_ia.parquet`

Base analítica consolidada da PNAD Contínua de 2020 a 2025, integrada aos indicadores de exposição à IA.

### `pnad_2020_2025_felten.parquet`

Base da PNAD filtrada para observações com AIOE preenchido.

### `pnad_2020_2025_gmyrek.parquet`

Base da PNAD filtrada para observações com indicadores de Gmyrek preenchidos.

### `agregado_felten_cod_ano.parquet`

Base agregada por ocupação, ano e trimestre contendo médias ponderadas do índice AIOE.

### `agregado_gmyrek_cod_ano.parquet`

Base agregada por ocupação, ano e trimestre contendo médias ponderadas dos indicadores de Gmyrek.

## Observação

Os microdados brutos da PNAD Contínua e os arquivos originais extensos da CBO não foram integralmente disponibilizados neste repositório por limitações de tamanho e reprodutibilidade. O repositório disponibiliza as bases finais tratadas utilizadas nas análises.
