# Span Alignment

### Steps

This folder contains code for extracting spans based on events from better basic data, aligning source and target spans, comparing silver and unsupervised spans, and creating input files for Turkle.

```bash
python silver_extract_spans.py -d <basic_silver_bp.json> -o <silver_output>
python gold_extract_spans.py -t <translation_file> -d <basic_gold_bp.json> -o <gold_output>
python unsupervised_span_alignment.py --input <gold_output> --source-lang en --target-lang ar --max-target-span-width <4> --output <unsup_output> --allow-overlap --decoding-method <greedy> --span-extractor <diffsum>
python get_stat.py -d <silver_output> -u <unsup_output> -i <gold_output> -o <output>
python process_for_turkle.py -d <output> -o <turkle_output>
```
