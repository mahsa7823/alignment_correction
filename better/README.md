1. \# reads human correction results (in a Turkle csv file) and extracts the corrected spans (sup_span)<br>
\# input: data/analysis-Batch_43_results.csv or data/train-Batch_results.csv <br>
\# output: sup_span.csv <br>
`python tkl_to_stat.py <analysis|train>`

2. \# combines source, silver, unsupervised, and supervised (corrected) spans in one file <br>
\# inputs: data/stat.out.{analysis|train}, sup_span.csv <br>
\# output: combine.csv <br>
`python sup_unsup.py <analysis|train>` 

3. \# compares silver, unsupervised, and supervised for statistics in Tab 3. <br>
\# The statistics in Tab 3 are printed out. <br>
\# input: combine.csv <br>
\# output: compare.csv <br>
`python compare_three.py <silver|unsup>`

4. \# build the semi-supervised bpjson file. Some manual edits are done on the output of this step to get the final bpjson file.<br>
`python make_bpjson.py`
