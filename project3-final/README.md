# Projeto Análise de Redes de Coexpressão em Cercárias de *Schistosoma mansoni*

# Project Co-expression Network Analysis in *Schistosoma mansoni* Cercariae

# Descrição Resumida do Projeto

Este projeto investigou padrões de expressão e coexpressão gênica em cercárias de *Schistosoma mansoni*, comparando amostras associadas a interações simpátricas e alopátricas com o hospedeiro intermediário. A proposta foi transformar dados públicos de RNA-seq em redes de coexpressão, explorar visualmente sua organização no Cytoscape e identificar módulos, hubs e genes candidatos biologicamente relevantes.

Após o controle de qualidade, a geração 1 foi excluída da análise principal por critério de qualidade, devido à contaminação identificada na amostra alopátrica SRR1142421. Para manter o pareamento, a amostra simpátrica correspondente também foi excluída. A análise final foi conduzida com as gerações 2 e 3.

A rede foi separada em duas camadas: uma rede positiva, representando genes positivamente coexpressos, e uma rede negativa, representando genes anticorrelacionados. As comunidades foram detectadas visualmente no Cytoscape com GLay.

# Slides

[Apresentação final em PDF](assets/slides/apresentacao-final.pdf)

# Fundamentação Teórica

O estudo parte da ideia de que interações parasita-hospedeiro podem estar associadas a alterações transcriptômicas em organismos parasitários. Em *Schistosoma mansoni*, cercárias representam um estágio relevante do ciclo de vida, associado à infecção do hospedeiro definitivo. A análise de redes de coexpressão permite observar não apenas genes isolados, mas módulos de genes com padrões coordenados ou opostos de expressão.

# Perguntas de Pesquisa

Pergunta principal: A interação simpátrica entre *Schistosoma mansoni* e seu hospedeiro intermediário está associada a padrões distintos de coexpressão gênica nas cercárias, em comparação com interações alopátricas?

Perguntas secundárias:

1. Quais genes apresentam padrões de coexpressão mais característicos em cercárias provenientes de interações simpátricas e alopátricas?
2. Existem módulos ou agrupamentos de genes coexpressos que diferenciam as duas condições experimentais?
3. Há diferenças na organização global das redes de coexpressão gênica entre cercárias simpátricas e alopátricas, considerando propriedades como conectividade e centralidade?

# Metodologia

A análise final utilizou amostras das gerações 2 e 3. A matriz TPM foi transformada por `log2(TPM + 1)`. Em seguida, foram selecionados genes/transcritos variáveis e calculadas correlações gene-gene.

Foram construídas duas redes:

- rede positiva: correlações positivas fortes;
- rede negativa: correlações negativas fortes.

Os arquivos de nós e arestas foram importados no Cytoscape. As comunidades foram detectadas com GLay. Em seguida, cada comunidade foi avaliada por conectividade, hubs, grau médio, anotação funcional e diferença média pareada entre alopátrico e simpátrico.

## Bases de Dados e Evolução

| Base | Endereço | Uso |
|---|---|---|
| SRA/ENA - SRP035609 | NCBI/ENA | dados públicos de RNA-seq |
| Referência *S. mansoni* PRJEA36577/WBPS19 | WormBase ParaSite/arquivo de referência | quantificação transcriptômica com Salmon |
| UniProt | https://www.uniprot.org/ | anotação funcional dos genes prioritários |

## Modelo Lógico

![Modelo lógico de grafos](assets/images/modelo-logico-grafos.png)

Modelo conceitual usado no projeto:

- Amostra possui condição;
- Amostra possui geração;
- Gene/transcrito é expresso em amostra;
- Gene/transcrito se conecta a outro gene/transcrito por correlação;
- Gene/transcrito pertence a comunidade GLay;
- Gene/transcrito possui métricas de centralidade;
- Gene/transcrito possui anotação funcional.

## Integração entre Bases

A integração principal ocorreu em três níveis: metadados das amostras, matriz de expressão e anotação funcional. Os IDs de genes/transcritos provenientes do Salmon foram usados para construir redes e, posteriormente, buscar anotações no UniProt. Os metadados permitiram classificar as amostras como simpátricas ou alopátricas e separar as gerações usadas na análise final.

## Análises Realizadas

As principais análises foram:

1. montagem da matriz TPM e NumReads;
2. exclusão da geração 1 por critério de qualidade;
3. construção de redes positiva e negativa;
4. detecção visual de comunidades com GLay no Cytoscape;
5. identificação de hubs e módulos centrais;
6. anotação funcional dos genes prioritários;
7. análise integrada de centralidade, conectividade e diferença pareada entre condições.

# Evolução do Projeto

O projeto evoluiu de uma análise inicial de expressão para uma abordagem de redes e visualização. Após o controle de qualidade, a geração 1 foi excluída da análise principal, tornando a abordagem mais conservadora. Também foi decidido separar correlações positivas e negativas, evitando misturar genes com comportamento coordenado e genes com comportamento inverso em uma única rede.

# Ferramentas

Foram usadas:

- FastQC e Trimmomatic nas etapas iniciais de qualidade;
- Salmon para quantificação transcriptômica;
- Python para manipulação de matrizes, construção das redes e síntese dos resultados;
- Cytoscape para visualização e detecção de comunidades com GLay;
- UniProt para anotação funcional.

# Resultados

Na rede positiva, o principal módulo foi a GLay 16, com 75 genes, 20 hubs e delta médio pareado positivo em alopátrico. Essa comunidade concentrou o núcleo central da rede positiva.

Outras comunidades positivas relevantes foram GLay 12, associada a proteínas secretadas, GLay 15, com sinal alopátrico forte, e GLay 3, com direção simpátrica forte.

Na rede negativa, as comunidades GLay 5 e GLay 6 concentraram os principais hubs de anticorrelação. Essas comunidades indicaram relações inversas envolvendo genes associados a membrana, tráfego vesicular, proteólise e processamento molecular.

# Discussão

A análise não permite afirmar de forma definitiva que as condições simpátrica e alopátrica possuem redes globalmente distintas, devido ao número reduzido de amostras após o controle de qualidade. Porém, a abordagem integrada de visualização, centralidade e anotação funcional permitiu identificar módulos candidatos.

O achado mais forte foi que a GLay 16, principal núcleo de coexpressão positiva, concentrou todos os hubs e apresentou maior atividade média na condição alopátrica. Além disso, módulos secundários apresentaram direções diferentes, indicando que a diferença entre condições não é global e uniforme, mas distribuída de forma heterogênea entre módulos.

# Conclusão

O projeto mostrou que a combinação de RNA-seq, redes de coexpressão, Cytoscape/GLay e anotação funcional permite identificar módulos e genes candidatos em dados transcriptômicos de *Schistosoma mansoni*. A análise final foi conservadora e exploratória, mas revelou um núcleo central de coexpressão positiva, módulos associados a proteínas secretadas e módulos de anticorrelação funcionalmente relevantes.

# Trabalhos Futuros

Como próximos passos, seria importante:

- aumentar o número de amostras por condição;
- validar os módulos em outros conjuntos de dados;
- realizar análise diferencial formal com contagens;
- usar bases específicas como WormBase ParaSite quando disponíveis;
- fazer enriquecimento funcional formal;
- comparar redes independentes por condição com maior número de réplicas.

# Referências Bibliográficas

Adicionar aqui as referências do artigo/dados originais, ferramentas usadas e bases de dados.
