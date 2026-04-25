import os
import pandas as pd # type: ignore



sample_map = {
    "SRR1140763": "Sym_1",
    "SRR1140994": "Sym_2",
    "SRR1140995": "Sym_3",
    "SRR1142421": "Allo_1",
    "SRR1142422": "Allo_2",
    "SRR1142423": "Allo_3",
}

tpm_dfs = []
reads_dfs = []

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
quant_dir = os.path.join(project_root, "data", "processed", "quant")
output_dir = os.path.join(project_root, "data", "processed")

for srr, sample-name in sample_map.items():
    path = os.path.join(quant_dir, srr, "quant.sf")
    df = pd.read_csv(path, sep="\t")

    tpm = df[["Name", "TPM"]].copy()
    tpm.columns = ["Name", sample_name]
    tpm_dfs.append(tpm)

    reads = df[["Name", "NumReads"]].copy()
    reads.columns = ["Name", sample_name]
    reads_dfs.append(reads)

tpm_matrix = tpm_dfs[0]
for df in tpm_dfs[1:]:
    tpm_matrix = tpm_matrix.merge(df, on="Name", how="outer")

reads_matrix = reads_dfs[0]
for df in reads_dfs[1:]:
    reads_matrix = reads_matrix.merge(df, on="Name", how="outer")

tpm_matrix = tpm_matrix.fillna(0)
reads_matrix = reads_matrix.fillna(0)

os.makedirs(output_dir, exist_ok=True)

tpm_out = os.path.join(output_dir, "matrix_tpm.csv")
reads_out = os.path.join(output_dir, "matrix_numreads.csv")

tpm_matrix.to_csv(tpm_out, index=False)
reads_matrix.to_csv(reads_out, index=False)

print("Arquivos gerados")
print(f"  - {tpm_out}")
print(f"  - {reads_out}")
