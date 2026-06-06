from pathlib import Path
import pandas as pd

raiz = Path(__file__).resolve().parents[1]

entrada_tpm = raiz / "data" / "processed" / "matrices" / "matrix_tpm.csv"
entrada_contagens = raiz / "data" / "processed" / "matrices" / "matrix_numreads.csv"

saida_base = raiz / "data" / "processed" / "limpo"
saida_matrizes = saida_base / "matrizes"
saida_metadados = saida_base / "metadata"

saida_matrizes.mkdir(parents=True, exist_ok=True)
saida_metadados.mkdir(parents=True, exist_ok=True)

amostras = pd.DataFrame([
    {"amostra": "SRR1140994", "condicao": "simpatrica", "geracao": 2},
    {"amostra": "SRR1140995", "condicao": "simpatrica", "geracao": 3},
    {"amostra": "SRR1142422", "condicao": "alopatrica", "geracao": 2},
    {"amostra": "SRR1142423", "condicao": "alopatrica", "geracao": 3},
])

colunas = ["Name"] + amostras["amostra"].tolist()

tpm = pd.read_csv(entrada_tpm)
tpm = tpm[colunas]
tpm.to_csv(saida_matrizes / "matrix_tpm_limpa.csv", index=False)

contagens = pd.read_csv(entrada_contagens)
contagens = contagens[colunas]
contagens.to_csv(saida_matrizes / "matrix_numreads_limpa.csv", index=False)

amostras.to_csv(saida_metadados / "amostras_limpas.csv", index=False)

print("ok")
