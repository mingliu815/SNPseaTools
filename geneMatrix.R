#' This is a R script to create a gene matrix from a single-cell RNA-seq dataset. 
#' The output will be a gzipped file (~.gct.gz), which can be used for SNPsea.
#' Rscript script.R input.Rdata output.gct

args <- commandArgs(trailingOnly = TRUE)
fileName <- args[1]
dataName <- args[2]
outputFile <- args[3]

load(fileName)
RNAseqData <- get(dataName)

num_row <- nrow(RNAseqData)
num_sample <- ncol(RNAseqData)

output <- data.frame(matrix(nrow = 3, ncol = num_sample + 2))
colnames(output) <- c("NAME", "Description", colnames(RNAseqData))
output[1,1] <- "#1.2"
output[2,1] <- num_row
output[2,2] <- num_sample
output[3, ] <- c("NAME", "Description", colnames(RNAseqData))

RNAseqData <- cbind(NAME = 1:dim(RNAseqData)[1], Description = rownames(RNAseqData), RNAseqData)
output <- rbind(output,RNAseqData)

write.table(output, file=outputFile, sep="\t", row.names=FALSE, col.names = FALSE, quote = FALSE, na = "")
system(paste("gzip ", outputFile))
