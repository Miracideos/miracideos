from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]

FINAL = RAIZ / "data" / "processed" / "limpo" / "final"
ANOTACAO = RAIZ / "data" / "processed" / "limpo" / "anotacao"

SAIDA_GENES = FINAL / "genes_interpretados_limpos.csv"
SAIDA_TEMAS = FINAL / "temas_por_glay_limpo.csv"
SAIDA_MD = FINAL / "resumo_final_limpo.md"


def primeiro(series):
    for valor in series:
        if pd.notna(valor) and str(valor).strip() not in ["", "nan", "NaN"]:
            return valor
    return ""


def tema(linha):
    texto = " ".join([
        str(linha.get("Protein names", "")),
        str(linha.get("Gene Ontology (biological process)", "")),
        str(linha.get("Gene Ontology (molecular function)", "")),
        str(linha.get("Function [CC]", "")),
        str(linha.get("InterPro", "")),
        str(linha.get("Pfam", "")),
    ]).lower()

    if any(x in texto for x in ["secret", "venom allergen", "allergen", "meg-"]):
        return "secrecao_interacao_hospedeiro"
    if any(x in texto for x in ["membrane", "surface", "tetraspanin", "tegument"]):
        return "membrana_superficie"
    if any(x in texto for x in ["cathepsin", "protease", "peptidase", "endopeptidase", "proteolysis"]):
        return "proteolise"
    if any(x in texto for x in ["zinc finger", "myb", "transcription", "dna binding", "ligase"]):
        return "regulacao_genica"
    if any(x in texto for x in ["cytochrome", "mitochond", "atp", "respiratory"]):
        return "mitocondria_energia"
    if any(x in texto for x in ["lipid", "palmitoyl", "phosphatidate", "diacylglycerol"]):
        return "lipidios_membrana"
    if any(x in texto for x in ["uncharacterized", "hypothetical"]):
        return "nao_caracterizado"
    return "outro_indefinido"


def carregar():
    anotacao = pd.read_csv(ANOTACAO / "anotacao_uniprot_integrada.csv")

    colunas = {
        "rede": "first",
        "glay": "first",
        "gene": "first",
        "degree": "first",
        "weighted_degree": "first",
        "hub_status": "first",
        "mean_log_expression": "first",
        "variance_log_expression": "first",
        "annotation_status": primeiro,
        "Entry": primeiro,
        "Entry Name": primeiro,
        "Reviewed": primeiro,
        "Protein names": primeiro,
        "Gene Names": primeiro,
        "Gene Ontology (biological process)": primeiro,
        "Gene Ontology (molecular function)": primeiro,
        "Gene Ontology (cellular component)": primeiro,
        "Function [CC]": primeiro,
        "InterPro": primeiro,
        "Pfam": primeiro,
    }

    colunas = {k: v for k, v in colunas.items() if k in anotacao.columns}

    genes = anotacao.groupby(["rede", "glay", "gene"], as_index=False).agg(colunas)
    genes["tema_funcional"] = genes.apply(tema, axis=1)

    genes = genes.sort_values(["rede", "glay", "degree", "weighted_degree"], ascending=[True, True, False, False])

    return genes


def escrever_md(genes, temas):
    linhas = []

    linhas.append("# Resumo final da reanalise limpa\n\n")
    linhas.append("A geracao 1 foi removida devido a contaminacao identificada na amostra alopatrica SRR1142421. A analise final foi feita com as geracoes 2 e 3.\n\n")
    linhas.append("Foram geradas duas redes separadas: uma rede positiva, usada como rede principal de coexpressao, e uma rede negativa, usada como analise complementar de anticorrelacao.\n\n")

    for rede in ["positiva", "negativa"]:
        sub_temas = temas[temas["rede"] == rede]
        sub_genes = genes[genes["rede"] == rede]

        linhas.append(f"## Rede {rede}\n\n")

        if len(sub_temas) == 0:
            linhas.append("Sem temas anotados.\n\n")
            continue

        principais = (
            sub_genes.groupby("glay")
            .agg(
                n_genes=("gene", "count"),
                n_hubs=("hub_status", lambda x: int((x == "hub").sum())),
                grau_medio=("degree", "mean"),
                gene_principal=("gene", "first"),
            )
            .reset_index()
            .sort_values(["n_hubs", "n_genes", "grau_medio"], ascending=False)
            .head(8)
        )

        linhas.append("### Comunidades prioritarias\n\n")

        for _, comunidade in principais.iterrows():
            glay = comunidade["glay"]
            linhas.append(f"### GLay {glay}\n\n")
            linhas.append(f"- genes prioritarios anotados: {comunidade['n_genes']}\n")
            linhas.append(f"- hubs anotados: {comunidade['n_hubs']}\n")
            linhas.append(f"- grau medio nos genes anotados: {comunidade['grau_medio']:.2f}\n")
            linhas.append(f"- gene principal anotado: {comunidade['gene_principal']}\n")

            t = sub_temas[sub_temas["glay"] == glay].sort_values("n_genes", ascending=False)

            if len(t) > 0:
                linhas.append("- temas:\n")
                for _, linha in t.iterrows():
                    linhas.append(f"  - {linha['tema_funcional']}: {linha['n_genes']}\n")

            genes_comunidade = sub_genes[sub_genes["glay"] == glay].sort_values("degree", ascending=False).head(8)

            linhas.append("- genes principais:\n")
            for _, gene in genes_comunidade.iterrows():
                produto = gene.get("Protein names", "")
                if pd.isna(produto) or str(produto).strip() == "":
                    produto = "sem anotacao clara"
                linhas.append(f"  - {gene['gene']} | grau {gene['degree']} | {produto} | {gene['tema_funcional']}\n")

            linhas.append("\n")

    SAIDA_MD.write_text("".join(linhas), encoding="utf-8")


def main():
    genes = carregar()

    temas = (
        genes[genes["annotation_status"].eq("found")]
        .groupby(["rede", "glay", "tema_funcional"])
        .size()
        .reset_index(name="n_genes")
        .sort_values(["rede", "glay", "n_genes"], ascending=[True, True, False])
    )

    genes.to_csv(SAIDA_GENES, index=False)
    temas.to_csv(SAIDA_TEMAS, index=False)
    escrever_md(genes, temas)

    print("Arquivos gerados:")
    print(SAIDA_GENES)
    print(SAIDA_TEMAS)
    print(SAIDA_MD)

    print("\nTemas principais:")
    print(temas.head(40).to_string(index=False))


if __name__ == "__main__":
    main()
