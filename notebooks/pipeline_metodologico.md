# Pipeline Metodológico

## Visão Geral

Este projeto teve como objetivo integrar índices internacionais de exposição à Inteligência Artificial às ocupações brasileiras e analisar seus impactos sobre o mercado de trabalho utilizando os microdados da PNAD Contínua.

## Etapas Metodológicas

### 1. Coleta de Dados

Foram coletadas informações provenientes das seguintes fontes:

- Classificação Brasileira de Ocupações (CBO 2002);
- Classificação de Ocupações para Pesquisas Domiciliares (COD);
- ISCO-88;
- ISCO-08;
- SOC 2010;
- Índice AIOE (Felten et al., 2021);
- Índices Exposure, Mean e SD (Gmyrek et al., 2025);
- Microdados da PNAD Contínua (2020–2025).

### 2. Extração e Tratamento Inicial

Foram extraídos dados de diferentes formatos de arquivos, incluindo planilhas, arquivos de texto, arquivos Parquet e documentos PDF. Essa etapa incluiu limpeza de colunas, padronização de nomes, tratamento de códigos ocupacionais e preparação das tabelas para compatibilização.

### 3. Harmonização Ocupacional Internacional

Foi realizada a compatibilização das classificações ocupacionais por meio da sequência:

```text
CBO → ISCO-88 → ISCO-08 → SOC 2010
```

Essa etapa permitiu conectar as ocupações brasileiras às classificações utilizadas nos estudos internacionais de exposição à IA.

### 4. Herança dos Indicadores Internacionais

Os índices de exposição à IA foram atribuídos às ocupações brasileiras por meio da compatibilização entre classificações ocupacionais equivalentes.

Foram utilizados:

- AIOE (Felten et al., 2021);
- Exposure;
- Mean;
- SD (Gmyrek et al., 2025).

### 5. Compatibilização CBO–COD

A integração com a PNAD foi realizada por meio de matching hierárquico entre CBO e COD, utilizando sucessivamente:

- Grupo de Base (4 dígitos);
- Subgrupo (3 dígitos);
- Subgrupo Principal (2 dígitos);
- Grande Grupo (1 dígito).

### 6. Fuzzy Matching

As ocupações remanescentes sem correspondência receberam tratamento por fuzzy matching utilizando a biblioteca RapidFuzz.

Foi utilizada a métrica `token_sort_ratio`, que calcula similaridade textual normalizada em escala de 0 a 100. Essa etapa foi aplicada principalmente às ocupações remanescentes sem AIOE após os métodos estruturais.

### 7. Embeddings Semânticos Residuais

Os embeddings foram utilizados apenas para casos residuais que permaneceram sem correspondência após os métodos anteriores.

Foi utilizado o modelo `text-embedding-3-large` da OpenAI com similaridade de cosseno. Os resultados foram submetidos à revisão manual e não foram incorporados automaticamente à base final.

### 8. Processamento da PNAD

Foram processados os microdados trimestrais da PNAD Contínua entre 2020 e 2025.

As etapas incluíram:

- Limpeza dos dados;
- Remoção de inconsistências;
- Filtros ocupacionais;
- Winsorização da renda;
- Transformação logarítmica da renda;
- Aplicação dos pesos amostrais.

### 9. Construção das Bases Finais

Foram geradas bases finais para análise:

- PNAD integrada ao índice AIOE;
- PNAD integrada aos indicadores Exposure, Mean e SD;
- Bases agregadas por ocupação, ano e trimestre.

### 10. Análises Estatísticas

Foram realizadas análises sobre:

- Distribuição dos indicadores de exposição;
- Matriz de correlação entre AIOE, Mean e SD;
- Exposição à IA e renda;
- Exposição à IA e gênero;
- Exposição à IA e localização;
- Evolução temporal da exposição;
- Top 20 e Bottom 20 ocupações mais e menos expostas.
