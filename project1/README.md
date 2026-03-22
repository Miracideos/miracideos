# Projeto `Análise de Redes de Coexpressão Gênica em Cercárias de Schistosoma mansoni sob Interações Simpátricas e Alopátricas`
# Project `Analysis of Gene Co-expression Networks in Schistosoma mansoni Cercariae under Sympatric and Allopatric Interactions`

# Descrição Resumida do Projeto

> A esquistossomose é uma doença parasitária de grande relevância em saúde pública, especialmente em regiões tropicais e subtropicais, sendo Schistosoma mansoni um de seus principais agentes etiológicos. No ciclo de vida desse parasita, o hospedeiro intermediário, representado por caramujos do gênero Biomphalaria, exerce papel fundamental no desenvolvimento das cercárias, forma infectante liberada no ambiente aquático. Nesse contexto, diferenças entre interações simpátricas, quando parasita e hospedeiro compartilham a mesma origem geográfica, e alopátricas, quando possuem origens distintas, podem influenciar processos biológicos importantes e deixar marcas detectáveis no perfil molecular das cercárias. A motivação deste projeto surge do interesse em investigar se essas diferentes interações estão associadas a padrões distintos de coexpressão gênica, permitindo representar esses comportamentos por meio de redes biológicas. Assim, o trabalho se insere na interface entre biologia, saúde e computação, utilizando dados de RNA-seq e análise de grafos para explorar, de forma introdutória, possíveis diferenças na organização transcriptômica de cercárias de Schistosoma mansoni sob condições simpátricas e alopátricas.

# Slides

> Coloque aqui o link para o PDF da apresentação da parte 1.

# Fundamentação Teórica

[1] **McManus, D. P., Dunne, D. W., Sacko, M., Utzinger, J., Vennervald, B. J., Zhou, X. N.** *Schistosomiasis*. Nature Reviews Disease Primers, 4, 13, 2018.  
  
Base para contextualizar a esquistossomose como problema de saúde pública e descrever o ciclo de vida de *Schistosoma mansoni*, com destaque para o papel do hospedeiro intermediário e do estágio de cercária no problema estudado.

[2] **Colley, D. G., Bustinduy, A. L., Secor, W. E., King, C. H.** *Human schistosomiasis*. The Lancet, 383(9936), 2253–2264, 2014.  
  
Base para reforçar a relevância biomédica da esquistossomose e a importância de compreender os mecanismos biológicos envolvidos na transmissão do parasita.

[3] **Portet, A., Pinaud, S., Chaparro, C., et al.** *Sympatric versus allopatric evolutionary contexts shape differential immune response in Biomphalaria/Schistosoma interaction*. PLOS Pathogens, 15(3), e1007647, 2019.  
  
Base para fundamentar a comparação entre interações simpátricas e alopátricas, mostrando que diferentes contextos evolutivos podem influenciar a interação entre *Biomphalaria* e *Schistosoma*.

[4] **Langfelder, P., Horvath, S.** *WGCNA: an R package for weighted correlation network analysis*. BMC Bioinformatics, 9, 559, 2008.  
  
Base para justificar o uso de redes de coexpressão gênica como abordagem de análise da organização transcriptômica nos dados do projeto.

# Perguntas de Pesquisa

> Pergunta principal: A interação simpátrica entre Schistosoma mansoni e seu hospedeiro intermediário está associada a padrões distintos de coexpressão gênica nas cercárias, em comparação com interações alopátricas?
> 
> Perguntas secundárias: Quais genes apresentam padrões de coexpressão mais característicos em cercárias provenientes de interações simpátricas e alopátricas? Existem módulos ou agrupamentos de genes coexpressos que diferenciam as duas condições experimentais? Há diferenças na organização global das redes de coexpressão gênica entre cercárias simpátricas e alopátricas, considerando propriedades como conectividade e centralidade?
> 
> Hipótese: Cercárias de Schistosoma mansoni originadas de interações simpátricas apresentam padrões de coexpressão gênica distintos daqueles observados em interações alopátricas, refletindo diferenças na organização transcriptômica associadas ao contexto biológico da interação parasita-hospedeiro.
> 
> Resultado esperado: Espera-se identificar, de forma exploratória, diferenças entre as redes de coexpressão gênica das cercárias em condições simpátricas e alopátricas. Em particular, espera-se observar, nas amostras simpátricas, redes com organização distinta, incluindo possíveis módulos gênicos mais definidos e genes com maior centralidade, potencialmente associados a processos biológicos relacionados à infecção e à adaptação ao hospedeiro.

# Bases de Dados

> | Base de Dados | Endereço na Web | Resumo |
> |---|---|---|
> | NCBI SRA – Experimentos SRX447203, SRX447380, SRX447381, SRX448442, SRX448443 e SRX448444 | https://www.ncbi.nlm.nih.gov/sra/SRX448444[accn]<br>https://www.ncbi.nlm.nih.gov/sra/SRX448443[accn]<br>https://www.ncbi.nlm.nih.gov/sra/SRX448442[accn]<br>https://www.ncbi.nlm.nih.gov/sra/SRX447381[accn]<br>https://www.ncbi.nlm.nih.gov/sra/SRX447380[accn]<br>https://www.ncbi.nlm.nih.gov/sra/SRX447203[accn] | Subconjunto operacional da base principal. Esses seis experimentos correspondem às bibliotecas que serão analisadas no projeto para comparar condições simpátricas e alopátricas em cercárias de *S. mansoni*. Eles serão usados para obtenção dos arquivos brutos de RNA-seq e construção das matrizes de expressão. Eles pertencem ao estudo SRP035609, que contém 6 itens de RNA dentro de um conjunto maior de experimentos públicos. |

# Modelo Lógico

> ![Modelo Lógico de Grafos](assets/images/modelologico.png)

# Metodologia
> 1. **Obtenção dos dados:** Os dados de RNA-seq serão obtidos a partir do repositório NCBI Sequence Read Archive (SRA), utilizando o SRA Toolkit. Serão selecionadas bibliotecas correspondentes às condições simpátricas e alopátricas previamente definidas no estudo de origem.
>
> 2. **Controle de qualidade:** A qualidade das reads será avaliada com o FastQC, considerando métricas como qualidade por base, conteúdo GC e presença de adaptadores. Os relatórios individuais serão integrados com o MultiQC para uma visão consolidada da qualidade dos dados.
>
> 3. **Quantificação da expressão gênica:** A quantificação da abundância de transcritos será realizada com o Salmon, utilizando pseudoalinhamento contra o transcriptoma de referência de *Schistosoma mansoni* (v10). Serão obtidas matrizes de expressão em termos de TPM e contagens brutas.

# Ferramentas

> **SRA Toolkit:** obtenção e conversão dos arquivos públicos de RNA-seq disponibilizados no NCBI SRA.
>
> **Ferramentas de controle de qualidade:**  
> **FastQC:** avaliação da qualidade das reads de sequenciamento.  
> **MultiQC:** agregação e visualização integrada dos relatórios de qualidade.  
> **Trimmomatic:** remoção de adaptadores e filtragem de reads de baixa qualidade, garantindo maior confiabilidade nas etapas subsequentes de análise.
>
> **Ferramentas de quantificação da expressão:**  
> **Salmon:** quantificação rápida e eficiente da abundância de transcritos, gerando valores de expressão, como TPM e contagens, sem necessidade de alinhamento completo ao genoma de referência.
>
> **Ferramentas de processamento e normalização dos dados:**  
> **Python:** manipulação, organização e preparação das matrizes de expressão para análise.  
> **pandas:** estruturação tabular e processamento dos dados obtidos nas etapas anteriores.  
>
> **Ferramentas de construção e análise das redes de coexpressão:**  
> **NetworkX:** modelagem computacional dos grafos e cálculo de propriedades estruturais das redes.  
> **Cytoscape:** visualização, exploração e interpretação das redes de coexpressão geradas.

# Referências Bibliográficas

>
> [1] McManus, D. P., Dunne, D. W., Sacko, M., Utzinger, J., Vennervald, B. J., Zhou, X. N. *Schistosomiasis*. Nature Reviews Disease Primers, v. 4, p. 13, 2018.
>
> [2] Colley, D. G., Bustinduy, A. L., Secor, W. E., King, C. H. *Human schistosomiasis*. The Lancet, v. 383, n. 9936, p. 2253–2264, 2014.
>
> [3] Portet, A., Pinaud, S., Chaparro, C., et al. *Sympatric versus allopatric evolutionary contexts shape differential immune response in Biomphalaria/Schistosoma interaction*. PLOS Pathogens, v. 15, n. 3, e1007647, 2019.
>
> [4] Andrews, S. *FastQC: A Quality Control Tool for High Throughput Sequence Data*. 2010. Available online at: http://www.bioinformatics.babraham.ac.uk/projects/fastqc
>
> [5] Ewels, P.; Magnusson, M.; Lundin, S.; Käller, M. *MultiQC: summarize analysis results for multiple tools and samples in a single report*. Bioinformatics, v. 32, n. 19, p. 3047–3048, 2016. DOI: 10.1093/bioinformatics/btw354.
>
> [6] Patro, R.; Duggal, G.; Love, M. I.; Irizarry, R. A.; Kingsford, C. *Salmon provides fast and bias-aware quantification of transcript expression*. Nature Methods, v. 14, n. 4, p. 417–419, 2017. DOI: 10.1038/nmeth.4197.