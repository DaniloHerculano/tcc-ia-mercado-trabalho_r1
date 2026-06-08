# Como Rodar as Análises Finais

Este repositório não reexecuta o pipeline completo desde os arquivos brutos, pois parte do processo depende de:

- arquivos PDF extensos da CBO;
- microdados pesados da PNAD Contínua;
- validação manual;
- ferramenta paga da OpenAI para embeddings.

O objetivo do notebook é reproduzir as análises finais a partir das bases tratadas já disponibilizadas no repositório.

## Arquivos necessários

Os arquivos esperados são:

```text
apendices/planilhas/cbo_final_com_felten_gmyrek_cod_FINAL_com_fuzzy.xlsx
apendices/parquet/pnad_2020_2025_analitica_ia.parquet
apendices/parquet/pnad_2020_2025_felten.parquet
apendices/parquet/pnad_2020_2025_gmyrek.parquet
apendices/parquet/agregado_felten_cod_ano.parquet
apendices/parquet/agregado_gmyrek_cod_ano.parquet
```

## Notebook

Use:

```text
notebooks/01_analises_finais_tcc.ipynb
```

Esse notebook permite:

- verificar se os arquivos existem;
- carregar as bases finais;
- calcular cobertura;
- gerar matriz de correlação;
- gerar distribuições de AIOE e Mean;
- gerar gráficos de renda versus exposição à IA;
- gerar rankings Top 20 e Bottom 20 ocupações.

## Observação

Caso o notebook seja executado no Google Colab, primeiro baixe o repositório ou carregue as pastas do GitHub no ambiente de execução.
