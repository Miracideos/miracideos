import os
import pandas as pd

base_dir = os.path.expanduser("~/quant")

samples = [
    "SRR1140763",
    "SRR1140994",
    "SRR1140995",
    "SRR1142421",
    "SRR1142422",
    "SRR1142423",
]

tpm_dfs = []
reads_dfs = []

for sample in samples:
    path = os.path.join(base_dir, sample, "quant.sf")
    df = pd.read_csv(path, sep="\t")

    tpm = df[["Name", "TPM"]].copy()
    tpm.columns = ["Name", sample]
    tpm_dfs.append(tpm)

    reads = df[["Name", "NumReads"]].copy()
    reads.columns = ["Name", sample]
    reads_dfs.append(reads)

tpm_matrix = tpm_dfs[0]
for df in tpm_dfs[1:]:
    tpm_matrix = tpm_matrix.merge(df, on="Name", how="outer")

reads_matrix = reads_dfs[0]
for df in reads_dfs[1:]:
    reads_matrix = reads_matrix.merge(df, on="Name", how="outer")

tpm_matrix = tpm_matrix.fillna(0)
reads_matrix = reads_matrix.fillna(0)

tpm_matrix.to_csv(os.path.join(base_dir, "matrix_tpm.csv"), index=False)
reads_matrix.to_csv(os.path.join(base_dir, "matrix_numreads.csv"), index=False)

print("Arquivos gerados:")
print(os.path.join(base_dir, "matrix_tpm.csv"))
print(os.path.join(base_dir, "matrix_numreads.csv"))
