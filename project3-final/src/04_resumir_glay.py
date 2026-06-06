from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]

CYTO = RAIZ / "data" / "processed" / "limpo" / "cytoscape"
FINAL = RAIZ / "data" / "processed" / "limpo" / "final"

FINAL.mkdir(parents=True, exist_ok=True)

ARQUIVOS = {
    "positiva": CYTO / "nos_cytoscape_positiva_com_glay.csv",
    "negativa": CYTO / "nos_cytoscape_negativa_com_glay.csv",
}


def achar_coluna(df, opcoes):
    for opcao in opcoes:
        if opcao in df.columns:
            return opcao
    raise ValueError(f"Coluna não encontrada. Procurei: {opcoes}. Achei: {df.columns.tolist()}")


def resumir(tipo, caminho):
    df = pd.read_csv(caminho)

    coluna_cluster = achar_coluna(df, ["__glayCluster", "glayCluster", "GLay Cluster", "cluster", "Cluster"])
    coluna_gene = achar_coluna(df, ["gene", "name", "shared name", "shared_name"])

    df = df.rename(columns={coluna_cluster: "glay", coluna_gene: "gene"})

    if "hub_status" not in df.columns:
        corte = df["degree"].quantile(0.95)
        df["hub_status"] = "non_hub"
        df.loc[df["degree"] >= corte, "hub_status"] = "hub"

    linhas = []

    for glay, grupo in df.groupby("glay"):
        ordenado = grupo.sort_values(["degree", "weighted_degree"], ascending=False)

        top_gene = ordenado.iloc[0]["gene"]
        top_degree = ordenado.iloc[0]["degree"]

        genes_principais = "; ".join(ordenado.head(10)["gene"].astype(str).tolist())

        linhas.append({
            "rede": tipo,
            "glay": glay,
            "n_genes": len(grupo),
            "n_hubs": int((grupo["hub_status"] == "hub").sum()),
            "mean_degree": grupo["degree"].mean(),
            "median_degree": grupo["degree"].median(),
            "max_degree": grupo["degree"].max(),
            "mean_weighted_degree": grupo["weighted_degree"].mean(),
            "top_gene": top_gene,
            "top_degree": top_degree,
            "genes_principais": genes_principais,
        })

    resumo = pd.DataFrame(linhas)
    resumo = resumo.sort_values(["n_hubs", "n_genes", "mean_degree"], ascending=False)

    df.to_csv(FINAL / f"genes_glay_{tipo}.csv", index=False)
    resumo.to_csv(FINAL / f"resumo_glay_{tipo}.csv", index=False)

    return df, resumo


def main():
    todos_resumos = []

    for tipo, caminho in ARQUIVOS.items():
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        genes, resumo = resumir(tipo, caminho)
        todos_resumos.append(resumo)

        print(f"\nRede {tipo}")
        print(resumo.head(15).to_string(index=False))

    geral = pd.concat(todos_resumos, ignore_index=True)
    geral.to_csv(FINAL / "resumo_glay_geral.csv", index=False)

    print("\nArquivos salvos em:")
    print(FINAL)


if __name__ == "__main__":
    main()
