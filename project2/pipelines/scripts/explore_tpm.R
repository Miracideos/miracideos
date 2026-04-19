tpm <- read.csv("~/quant/matrix_tpm.csv", check.names = FALSE)

rownames(tpm) <- tpm$Name
tpm$Name <- NULL

tpm_log <- log2(tpm + 1)

# selecionar genes mais variáveis
vars <- apply(tpm_log, 1, var)

# pegar top 100
top_genes <- names(sort(vars, decreasing = TRUE))[1:100]

tpm_top <- tpm_log[top_genes, ]

# normalizar (z-score por gene)
tpm_scaled <- t(scale(t(tpm_top)))

# salvar heatmap
pdf("~/quant/heatmap_top_genes.pdf", width = 10, height = 10)

heatmap(
  tpm_scaled,
  scale = "none",
  col = colorRampPalette(c("blue", "white", "red"))(50),
  main = "Top 100 genes mais variáveis"
)

dev.off()

cat("Heatmap salvo em ~/quant/heatmap_top_genes.pdf\n")
