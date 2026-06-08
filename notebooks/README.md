# TCC — Inteligência Artificial e Mercado de Trabalho Brasileiro

Este repositório documenta os códigos, bases tratadas e resultados utilizados no Trabalho de Conclusão de Curso sobre exposição das ocupações brasileiras à inteligência artificial.

O objetivo do projeto é integrar indicadores internacionais de exposição à IA, especialmente os índices de Felten et al. (2021) e Gmyrek et al. (2025), aos microdados da PNAD Contínua de 2020 a 2025, por meio de compatibilização entre classificações ocupacionais brasileiras e internacionais.

## Estrutura do repositório

- `notebooks/`: notebooks e arquivos utilizados para documentar e reproduzir as análises finais.
- `apendices/planilhas/`: planilhas finais e intermediárias do processo de harmonização ocupacional.
- `apendices/parquet/`: bases finais em formato Parquet utilizadas nas análises.
- `src/`: código da aplicação existente no projeto. Esta pasta não foi alterada para a documentação metodológica do TCC.

## Como reproduzir as análises finais

As análises finais podem ser reproduzidas a partir do notebook:

```text
notebooks/01_analises_finais_tcc.ipynb
```

Esse notebook utiliza os arquivos finais já tratados nas pastas:

```text
apendices/planilhas/
apendices/parquet/
```

## Observações sobre reprodutibilidade

Este repositório disponibiliza as bases finais, os notebooks de análise e a documentação metodológica utilizados no Trabalho de Conclusão de Curso. As análises estatísticas e os principais resultados podem ser reproduzidos a partir dos arquivos disponibilizados em `apendices/planilhas` e `apendices/parquet`.

Entretanto, a reprodução integral do pipeline original apresenta algumas limitações práticas:

- Parte do processamento inicial exigiu a extração e tratamento de grandes volumes de dados provenientes dos livros da Classificação Brasileira de Ocupações (CBO), originalmente disponibilizados em arquivos PDF extensos.
- O processamento dos microdados da PNAD Contínua envolveu dezenas de arquivos trimestrais e a geração de bases consolidadas em formato Parquet de grande porte, o que demanda capacidade significativa de armazenamento e processamento.
- A etapa de uso dos embeddings semânticos nas ocupações restantes sem índices de exposição à IA utilizou o modelo `text-embedding-3-large` da OpenAI. Essa ferramenta depende de credenciais privadas de acesso (API Key), possui uso controlado pelo provedor e gera custos financeiros proporcionais ao volume de processamento realizado.
- Por razões de custo, segurança e restrições de acesso, as credenciais utilizadas não são disponibilizadas neste repositório.
- Além disso, os embeddings foram empregados apenas como etapa complementar de análise e validação para ocupações sem correspondência pelos métodos principais, não tendo sido incorporados automaticamente à base final utilizada nas análises estatísticas.

Dessa forma, o repositório tem como objetivo principal documentar a metodologia empregada, disponibilizar os dados tratados e permitir a reprodução dos resultados finais apresentados no trabalho.

## Principais bases finais

- `cbo_final_com_felten_gmyrek_cod_FINAL_com_fuzzy.xlsx`
- `pnad_2020_2025_analitica_ia.parquet`
- `pnad_2020_2025_felten.parquet`
- `pnad_2020_2025_gmyrek.parquet`
- `agregado_felten_cod_ano.parquet`
- `agregado_gmyrek_cod_ano.parquet`

## Observação metodológica

Os resultados finais utilizados nas análises estatísticas foram obtidos principalmente por compatibilização ocupacional, herança de indicadores, matching hierárquico e fuzzy matching validado. Os resultados obtidos através dos embeddings semânticos não foram incorporados à base final. 
