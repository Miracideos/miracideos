# Como entender o repositório

Este repositório foi organizado para facilitar a navegação, compreensão e reprodução do pipeline de RNA-seq realizado no projeto.

## Estrutura geral

O projeto está dividido em quatro partes principais:

- `scripts/`: contém todos os códigos utilizados na análise
- `results/`: reúne os resultados finais e intermediários
- `qc/`: inclui relatórios de controle de qualidade
- `data_info/`: contém informações sobre as amostras

## Scripts

A pasta `scripts/` contém os arquivos responsáveis pela execução do pipeline, incluindo:

- construção de matrizes de expressão
- análise exploratória (correlação, PCA)
- análise diferencial

Esses scripts permitem reproduzir toda a análise a partir dos dados.

## Resultados

A pasta `results/` está subdividida em:

- `matrices/`: dados numéricos (TPM, correlação, PCA)
- `plots/`: visualizações (heatmap, gráficos exploratórios)
- `differential/`: resultados da análise diferencial

Esses arquivos representam os principais outputs do projeto.

## Controle de qualidade

A pasta `qc/` contém relatórios do FastQC antes e depois do trimming. Esses arquivos permitem verificar a qualidade dos dados e a efetividade do pré-processamento.

## Informações das amostras

A pasta `data_info/` contém informações básicas sobre os dados utilizados, incluindo:

- lista de amostras
- observações relevantes sobre qualidade ou comportamento

## Como navegar

Para entender rapidamente o projeto, recomenda-se:

1. Começar pelos gráficos em `results/plots/`
2. Consultar as matrizes em `results/matrices/`
3. Verificar resultados diferenciais em `results/differential/`
4. Revisar os scripts para entender como a análise foi conduzida

Essa estrutura permite tanto uma visão geral dos resultados quanto a reprodução completa do pipeline.