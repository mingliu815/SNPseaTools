# SNPsea

[SNPsea](http://pubs.broadinstitute.org/mpg/snpsea/) is an algorithm to identify cell types and pathways affected by risk loci.

These are tools for generating SNPsea analysis.

- geneMatrix.R (code above)

This is a script in R to create our own gene matrix from a single-cell RNA-seq dataset. Output will be automatically gzipped (~.gct.gz).

Run `Rscript geneMatrix.R original_dataset.RData name_of_single-cell-RNA-seq output.gct`

- snpsea-barplot 

This is a revised version for snpsea-barplot which are suitable for our python. Original code can be found [here](https://github.com/slowkow/snpsea).

Run `python snpsea-barplot out`

- proxyReplace.py (code above)

This is a script in Python to find proxy SNPs of index SNPs who are absent in their reference data (*/snpsea/TGP2011.bed.gz*). We consider SNPs who are in reference data with the highest R^2 as proxy SNPs of index SNPs. It will replace chr, pos, and rsID with information of proxy SNPs but keep p-values as the original. It will also include a column of R^2 in output gwas file. If SNPs are not replaced, R^2 is NA.

Run `python proxyReplace.py --input input.gwas --output output.gwas` 
