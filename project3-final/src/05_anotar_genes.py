from pathlib import Path
from io import StringIO
import time

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parents[1]

FINAL = RAIZ / "data" / "processed" / "limpo" / "final"
ANOTACAO = RAIZ / "data" / "processed" / "limpo" / "anotacao"

ANOTACAO.mkdir(parents=True, exist_ok=True)

ORGANISMO = "6183"
URL = "https://rest.uniprot.org/uniprotkb/search"


def normalizar(gene):
    gene = str(gene).strip()
    if "." in gene:
        return gene.rsplit(".", 1)[0]
    return gene


def juntar_motivos(tabela):
    motivos = (
        tabela.groupby("gene")["motivo_prioridade"]
        .apply(lambda x: ";".join(sorted(set(x))))
        .reset_index()
    )

    tabela = tabela.drop_duplicates(subset=["gene"]).drop(columns=["motivo_prioridade"])
    tabela = tabela.merge(motivos, on="gene", how="left")

    return tabela


def carregar_rede(arquivo, rede):
    df = pd.read_csv(arquivo)
    df["rede"] = rede

    partes = []

    if "hub_status" in df.columns:
        hubs = df[df["hub_status"] == "hub"].copy()
        hubs["motivo_prioridade"] = "hub"
        partes.append(hubs)

    top_grau = (
        df.sort_values(["degree", "weighted_degree"], ascending=False)
        .head(50)
        .copy()
    )
    top_grau["motivo_prioridade"] = "top_grau_rede"
    partes.append(top_grau)

    if "glay" in df.columns:
        top_glay = (
            df.sort_values(["glay", "degree", "weighted_degree"], ascending=[True, False, False])
            .groupby("glay")
            .head(5)
            .copy()
        )
        top_glay["motivo_prioridade"] = "top5_por_glay"
        partes.append(top_glay)

    if "delta_medio_pareado" in df.columns:
        top_delta = df.reindex(
            df["delta_medio_pareado"].abs().sort_values(ascending=False).index
        ).head(40).copy()
        top_delta["motivo_prioridade"] = "top_delta"
        partes.append(top_delta)

    if "delta_allopatric_minus_sympatric" in df.columns:
        top_delta = df.reindex(
            df["delta_allopatric_minus_sympatric"].abs().sort_values(ascending=False).index
        ).head(40).copy()
        top_delta["motivo_prioridade"] = "top_delta"
        partes.append(top_delta)

    prioridade = pd.concat(partes, ignore_index=True)
    prioridade = juntar_motivos(prioridade)
    prioridade["gene_busca"] = prioridade["gene"].apply(normalizar)

    return prioridade


def carregar_prioritarios():
    arquivos = [
        (FINAL / "genes_glay_positiva.csv", "positiva"),
        (FINAL / "genes_glay_negativa.csv", "negativa"),
    ]

    partes = []

    for arquivo, rede in arquivos:
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

        partes.append(carregar_rede(arquivo, rede))

    prioridade = pd.concat(partes, ignore_index=True)

    motivos = (
        prioridade.groupby(["gene", "rede"])["motivo_prioridade"]
        .apply(lambda x: ";".join(sorted(set(";".join(x).split(";")))))
        .reset_index()
    )

    prioridade = prioridade.drop_duplicates(subset=["gene", "rede"]).drop(columns=["motivo_prioridade"])
    prioridade = prioridade.merge(motivos, on=["gene", "rede"], how="left")

    prioridade.to_csv(ANOTACAO / "genes_prioritarios_limpos.csv", index=False)

    return prioridade


def buscar(gene):
    campos = ",".join([
        "accession",
        "id",
        "reviewed",
        "protein_name",
        "gene_names",
        "organism_name",
        "go_p",
        "go_f",
        "go_c",
        "cc_function",
        "xref_interpro",
        "xref_pfam",
    ])

    consultas = [
        f"(gene_exact:{gene}) AND (organism_id:{ORGANISMO})",
        f"({gene}) AND (organism_id:{ORGANISMO})",
    ]

    for consulta in consultas:
        resposta = requests.get(
            URL,
            params={
                "query": consulta,
                "format": "tsv",
                "fields": campos,
                "size": 3,
            },
            timeout=30,
        )

        if resposta.status_code != 200:
            continue

        texto = resposta.text.strip()

        if not texto:
            continue

        linhas = texto.splitlines()

        if len(linhas) <= 1:
            continue

        df = pd.read_csv(StringIO(texto), sep="\t")
        df.insert(0, "gene_busca", gene)
        df["annotation_status"] = "found"
        return df

    return pd.DataFrame([{
        "gene_busca": gene,
        "Entry": "",
        "Entry Name": "",
        "Reviewed": "",
        "Protein names": "",
        "Gene Names": "",
        "Organism": "",
        "Gene Ontology (biological process)": "",
        "Gene Ontology (molecular function)": "",
        "Gene Ontology (cellular component)": "",
        "Function [CC]": "",
        "InterPro": "",
        "Pfam": "",
        "annotation_status": "not_found",
    }])


def main():
    prioritarios = carregar_prioritarios()

    genes = sorted(prioritarios["gene_busca"].dropna().unique().tolist())

    resultados = []

    for i, gene in enumerate(genes, start=1):
        print(f"{i}/{len(genes)} {gene}")
        resultados.append(buscar(gene))
        time.sleep(0.25)

    anotacao = pd.concat(resultados, ignore_index=True)
    anotacao.to_csv(ANOTACAO / "anotacao_uniprot_bruta.csv", index=False)

    integrada = prioritarios.merge(anotacao, on="gene_busca", how="left")
    integrada.to_csv(ANOTACAO / "anotacao_uniprot_integrada.csv", index=False)

    print("\nGenes priorizados:")
    print(len(prioritarios))

    print("\nResumo:")
    print(integrada["annotation_status"].fillna("missing").value_counts())

    print("\nMotivos de prioridade:")
    print(integrada["motivo_prioridade"].value_counts().head(20))

    print("\nArquivo salvo em:")
    print(ANOTACAO / "anotacao_uniprot_integrada.csv")


if __name__ == "__main__":
    main()
