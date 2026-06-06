from pathlib import Path
import pandas as pd
import numpy as np

RAIZ = Path(__file__).resolve().parents[1]

MATRIZ = RAIZ / "data" / "processed" / "limpo" / "matrizes" / "matrix_tpm_limpa.csv"
CYTO = RAIZ / "data" / "processed" / "limpo" / "cytoscape"
FINAL = RAIZ / "data" / "processed" / "limpo" / "final"

FINAL.mkdir(parents=True, exist_ok=True)

AMOSTRAS = {
    "simpatrica": ["SRR1140994", "SRR1140995"],
    "alopatrica": ["SRR1142422", "SRR1142423"],
}

ARQUIVOS = {
    "positiva": CYTO / "nos_cytoscape_positiva_com_glay.csv",
    "negativa": CYTO / "nos_cytoscape_negativa_com_glay.csv",
}


def achar_coluna(df, opcoes):
    for opcao in opcoes:
        if opcao in df.columns:
            return opcao
    raise ValueError(f"Coluna não encontrada: {opcoes}")


def carregar_expressao():
    matriz = pd.read_csv(MATRIZ)
    matriz = matriz.set_index("Name")
    matriz = matriz.apply(pd.to_numeric, errors="coerce").fillna(0)
    log = np.log2(matriz + 1)

    resultado = pd.DataFrame(index=log.index)
    resultado["media_simpatrica"] = log[AMOSTRAS["simpatrica"]].mean(axis=1)
    resultado["media_alopatrica"] = log[AMOSTRAS["alopatrica"]].mean(axis=1)
    resultado["delta_alopatrica_menos_simpatrica"] = resultado["media_alopatrica"] - resultado["media_simpatrica"]
    resultado["abs_delta"] = resultado["delta_alopatrica_menos_simpatrica"].abs()
    resultado["delta_geracao_2"] = log["SRR1142422"] - log["SRR1140994"]
    resultado["delta_geracao_3"] = log["SRR1142423"] - log["SRR1140995"]
    resultado["delta_medio_pareado"] = resultado[["delta_geracao_2", "delta_geracao_3"]].mean(axis=1)
    resultado["abs_delta_medio_pareado"] = resultado["delta_medio_pareado"].abs()
    resultado = resultado.reset_index().rename(columns={"Name": "gene"})

    return resultado


def carregar_rede(caminho, rede, expressao):
    df = pd.read_csv(caminho)

    coluna_gene = achar_coluna(df, ["gene", "name", "shared name", "shared_name"])
    coluna_glay = achar_coluna(df, ["glay", "__glayCluster", "glayCluster", "GLay Cluster", "cluster", "Cluster"])

    df = df.rename(columns={coluna_gene: "gene", coluna_glay: "glay"})
    df["rede"] = rede

    if "hub_status" not in df.columns:
        corte = df["degree"].quantile(0.95)
        df["hub_status"] = "non_hub"
        df.loc[df["degree"] >= corte, "hub_status"] = "hub"

    df = df.merge(expressao, on="gene", how="left")

    return df


def direcao(valor):
    if pd.isna(valor):
        return "sem_delta"
    if valor >= 1:
        return "maior_alopatrica_forte"
    if valor >= 0.5:
        return "maior_alopatrica_moderado"
    if valor <= -1:
        return "maior_simpatrica_forte"
    if valor <= -0.5:
        return "maior_simpatrica_moderado"
    return "diferenca_pequena"


def resumir_modulos(df):
    linhas = []

    for (rede, glay), grupo in df.groupby(["rede", "glay"]):
        hubs = grupo[grupo["hub_status"] == "hub"]

        top = grupo.sort_values(["degree", "weighted_degree"], ascending=False).iloc[0]

        peso = grupo["degree"].clip(lower=1)
        delta_ponderado = np.average(grupo["delta_medio_pareado"].fillna(0), weights=peso)

        linhas.append({
            "rede": rede,
            "glay": glay,
            "n_genes": len(grupo),
            "n_hubs": len(hubs),
            "grau_medio": grupo["degree"].mean(),
            "grau_maximo": grupo["degree"].max(),
            "weighted_degree_medio": grupo["weighted_degree"].mean(),
            "top_gene": top["gene"],
            "top_gene_degree": top["degree"],
            "media_delta_pareado": grupo["delta_medio_pareado"].mean(),
            "mediana_delta_pareado": grupo["delta_medio_pareado"].median(),
            "media_abs_delta_pareado": grupo["abs_delta_medio_pareado"].mean(),
            "delta_ponderado_por_grau": delta_ponderado,
            "direcao_modulo": direcao(grupo["delta_medio_pareado"].mean()),
            "media_delta_hubs": hubs["delta_medio_pareado"].mean() if len(hubs) else np.nan,
            "genes_principais": "; ".join(grupo.sort_values(["degree", "weighted_degree"], ascending=False).head(8)["gene"].astype(str)),
        })

    resumo = pd.DataFrame(linhas)
    resumo = resumo.sort_values(["rede", "n_hubs", "grau_medio", "media_abs_delta_pareado"], ascending=[True, False, False, False])

    return resumo


def resumir_hubs(df):
    hubs = df[df["hub_status"] == "hub"].copy()
    hubs = hubs.sort_values(["rede", "degree", "weighted_degree"], ascending=[True, False, False])
    return hubs


def escrever_md(modulos, hubs):
    linhas = []

    linhas.append("# Conectividade, centralidade e condição\n\n")
    linhas.append("A análise avaliou conectividade e centralidade na rede limpa usando as comunidades GLay das redes positiva e negativa. A comparação entre condições foi feita pela diferença média pareada entre alopátrico e simpátrico nas gerações 2 e 3.\n\n")

    for rede in ["positiva", "negativa"]:
        sub = modulos[modulos["rede"] == rede].copy()
        sub_hubs = hubs[hubs["rede"] == rede].copy()

        linhas.append(f"## Rede {rede}\n\n")
        linhas.append(f"- comunidades avaliadas: {sub['glay'].nunique()}\n")
        linhas.append(f"- hubs avaliados: {len(sub_hubs)}\n\n")

        linhas.append("### Módulos mais centrais\n\n")

        for _, linha in sub.head(6).iterrows():
            linhas.append(f"- GLay {linha['glay']}: {linha['n_genes']} genes, {linha['n_hubs']} hubs, grau médio {linha['grau_medio']:.2f}, top gene {linha['top_gene']}, delta médio pareado {linha['media_delta_pareado']:.3f}, direção {linha['direcao_modulo']}.\n")

        linhas.append("\n### Hubs principais\n\n")

        for _, linha in sub_hubs.head(10).iterrows():
            linhas.append(f"- {linha['gene']}: GLay {linha['glay']}, grau {linha['degree']}, delta médio pareado {linha['delta_medio_pareado']:.3f}.\n")

        linhas.append("\n")

    FINAL_MD = FINAL / "resumo_centralidade_condicao.md"
    FINAL_MD.write_text("".join(linhas), encoding="utf-8")


def main():
    expressao = carregar_expressao()

    redes = []

    for rede, arquivo in ARQUIVOS.items():
        if not arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        redes.append(carregar_rede(arquivo, rede, expressao))

    dados = pd.concat(redes, ignore_index=True)

    modulos = resumir_modulos(dados)
    hubs = resumir_hubs(dados)

    dados.to_csv(FINAL / "genes_com_centralidade_e_condicao.csv", index=False)
    modulos.to_csv(FINAL / "centralidade_condicao_por_glay.csv", index=False)
    hubs.to_csv(FINAL / "centralidade_condicao_hubs.csv", index=False)

    escrever_md(modulos, hubs)

    print("Arquivos gerados:")
    print(FINAL / "genes_com_centralidade_e_condicao.csv")
    print(FINAL / "centralidade_condicao_por_glay.csv")
    print(FINAL / "centralidade_condicao_hubs.csv")
    print(FINAL / "resumo_centralidade_condicao.md")

    print("\nMódulos principais:")
    print(modulos.head(20).to_string(index=False))

    print("\nHubs principais:")
    print(hubs[["rede", "glay", "gene", "degree", "weighted_degree", "delta_medio_pareado"]].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
