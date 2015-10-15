https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_norm.py#L83-L84
`rscript += "write.table(rnaseq_sig, file='{2}/{0}_vs_{1}_deseq2_significant.tsv', sep='\\t', quote=F)\n".format(cond1, cond2, outdir)

rscript += "write.table(rnaseq_res, file='{2}/{0}_vs_{1}_deseq2_analysis.tsv', sep='\\t', quote=F)\n".format(cond1, cond2, outdir)`
