# Execução dos scripts

Ambiente usado no desenvolvimento: Python com `pandas`, `numpy`, `networkx`, `requests` e Cytoscape para visualização.

Instalação mínima:

```bash
pip install pandas numpy networkx requests
```

Ordem da análise final:

```bash
python 01_filtrar_amostras.py
python 02_montar_redes.py
```

Depois dessas duas etapas, importar no Cytoscape os arquivos:

```text
data/processed/cytoscape/arestas_cytoscape_positiva.csv
data/processed/cytoscape/nos_cytoscape_positiva.csv
data/processed/cytoscape/arestas_cytoscape_negativa.csv
data/processed/cytoscape/nos_cytoscape_negativa.csv
```

Rodar o GLay no Cytoscape para as duas redes e exportar as tabelas de nós como:

```text
data/processed/cytoscape/nos_cytoscape_positiva_com_glay.csv
data/processed/cytoscape/nos_cytoscape_negativa_com_glay.csv
```

Depois rodar:

```bash
python 04_resumir_glay.py
python 05_anotar_genes.py
python 06_resumo_final.py
python 07_centralidade_condicao.py
```

O script `make_matrix.py` é mantido como registro da etapa que consolidou os arquivos `quant.sf` do Salmon em matrizes de expressão.
