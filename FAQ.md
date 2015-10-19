https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_norm.py#L83-L84 :

 * Is this running DESeq on the ATAC-seq reads? Only using it for the
 normalisation right?

 This function is not fully functional. I was testing different normalisation strategies such as CQN normalisation.

 * Why save the results from DESeq if this was only used to get the PCA?

 Legacy code, I copied this from another function, ignore this. In fact this entire function is not important

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_norm.py#L94 :

 * What is featureCounts? Why do you keep only counts[,6:ncol(counts)]? What are the columns 1:5?
 
FeatureCounts is an alternative to htseq-count and part of the subread package: http://subread.sourceforge.net/ It is much faster than htseq-counts, the first 5 columns contain some unimportant information about the counted features

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_norm.py#L116 :

 * What file is this documented in?
 
 Its copied from another package, from this package: https://github.com/pdl30/pyrnatools And an example of the config: https://github.com/pdl30/pyrnatools/blob/master/Configuration_examples/example_config.ini

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_norm.py#L94 :

 * What and why needs to be changed?
Dosen't matter, I was looking into better ways of running this script so that I could parallelise multiple comparisons, I never got around to it. My comments leave alot to be desired.
I don't think this script is useful/necessary for you.

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L61 :

 * I don't understand why calculate the coverage on a single base here.

Its to test if the chromosome exists, not to do any coverage counting

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L88 :

 * tmp1 is a dictionary of sorted positions (keys) covered by reads (values is the coverage). Aggreagated_cvg is the coverage at those poisitions over all TSSs.
 Why multiply by 10000? 

 * No major reason, to make the values on the plots easier to read

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L127 :

 * Obviously this is not a GTF file otherewise the name wouldn't be the first
 field. What format is the annotation file?

 * This is the format found in the data directory i.e. https://github.com/mxenoph/pyatactools/blob/master/pyatactools/data/mm10_ensembl_80.txt

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L135 :

 * What's mRNA_len_cut?
 * If the mRNA is less than 100bp in length, then it is not included in the genebody plot

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L162-170 :
 
 * Don't understand why leaving a 10bp gap between the 1kb upstream the TSS and
 10bp after the TTS.
 * Can't remember the reason for this but it has something to do with plotting. Feel free to look further into this

https://github.com/mxenoph/pyatactools/blob/mx-dev/pyatactools/atac_profiler.py#L165 :

 * shouldn't it be `if before < 0`
 * Are you sure this is the right line? Don't know what you are referring to.
