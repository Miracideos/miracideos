tpm <- read.csv("~/quant/matrix_tpm.csv", check.names = FALSE)

rownames(tpm) <- tpm$Name
tpm$Name <- NULL

tpm_log <- log2(tpm + 1)

target_sample <- "SRR1142421"
other_samples <- setdiff(colnames(tpm_log), target_sample)

others_mean <- rowMeans(tpm_log[, other_samples, drop = FALSE])

result <- data.frame(
  Gene = rownames(tpm_log),
  Target = tpm_log[, target_sample],
  OthersMean = others_mean,
  Log2FC = tpm_log[, target_sample] - others_mean
)

upregulated <- result[order(result$Log2FC, decreasing = TRUE), ]
downregulated <- result[order(result$Log2FC, decreasing = FALSE), ]

write.csv(result, "~/quant/diff_SRR1142421_vs_others_all.csv", row.names = FALSE)
write.csv(head(upregulated, 20), "~/quant/diff_SRR1142421_top20_up.csv", row.names = FALSE)
write.csv(head(downregulated, 20), "~/quant/diff_SRR1142421_top20_down.csv", row.names = FALSE)

cat("Top 10 genes mais aumentados em", target_sample, ":\n")
print(head(upregulated[, c("Gene", "Log2FC", "Target", "OthersMean")], 10))

cat("\nTop 10 genes mais reduzidos em", target_sample, ":\n")
print(head(downregulated[, c("Gene", "Log2FC", "Target", "OthersMean")], 10))
