# Código‑fonte do projeto

Este diretório contém todos os scripts utilizados no pipeline de análise de RNA‑seq de *Schistosoma mansoni* (comparação entre condições simpátricas e alopátricas).

## Scripts disponíveis

| Script                     | Descrição                                                                 |
|----------------------------|----------------------------------------------------------------------------|
| `run_trimming.bat`         | Aplica Trimmomatic para corte de adaptadores e filtro de qualidade.        |
| `run_fastqc_trimmed.bat`   | Gera relatórios FastQC dos arquivos pós‑trimming.                          |
| `run_salmon.bat`           | Executa a quantificação de expressão com Salmon (mode `quant`).            |
| `make_matrix.py`           | Agrega os arquivos `quant.sf` em matrizes de TPM e contagens.              |
| `diff_simple.R`            | Análise exploratória de expressão diferencial (a ser executado manualmente). |
| `explore_tpm.R`            | Visualização dos dados de TPM (PCA, heatmaps, etc.).                       |

## Pré‑requisitos

- **Windows** (os scripts `.bat` utilizam sintaxe do cmd).
- **SRA Toolkit** (`fastq-dump`) – disponível no `PATH`.
- **Trimmomatic** (≥ 0.40) – ajuste o caminho do `.jar` dentro do script.
- **FastQC** – instalado e acessível via linha de comando.
- **Salmon** (≥ 1.10) – executável no `PATH` ou com caminho completo definido no script.
- **Python 3** com `pandas` instalado.
- **R** com os pacotes necessários para os scripts `.R` (opcional).

## Como executar

Os scripts são orquestrados pelo arquivo `main.bat` localizado **na raiz do projeto**.
Para rodar o pipeline completo:

```cmd
cd caminho\para\project2\src\
main.bat
