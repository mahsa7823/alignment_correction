import argparse
import itertools
import math
import random

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--silver', required=True)
  parser.add_argument('--unsup', required=True)
  parser.add_argument('--gold', required=True)
  parser.add_argument('--keep-proportion', type=float, help='proportion of gold data to sample (between 0 and 1)')
  parser.add_argument('--keep-quantity', type=int, help='number of gold data to sample')
  parser.add_argument('--seeds', required=True, nargs='+', type=int, help='list of seeds')
  
  args = parser.parse_args()

  return args

def load_data(data_file):
  with open(data_file, "r", encoding="utf-8") as f:
    file_contents = f.read()
  lines = file_contents.splitlines()
  grouped_data = [list(g) for k,g in itertools.groupby(lines, key=lambda x: x=='')]
  sentence_data = [s for s in grouped_data if s != ['']]
  sentence_data = sentence_data[1:]  # skip "-DOCSTART-" line at top of file
  sentence_data = {i: d for i,d in enumerate(sentence_data)}

  return sentence_data

def sentence_disagreement(silver, unsup):
  # Whether the predictions for the sentence differ enough
  # that we should "send the sentence for annotation"
  return silver != unsup

def get_disagreement_sentence_ids(silver_data, unsup_data):
  disagreement_sentence_ids = []
  sentence_ids = silver_data.keys() | unsup_data.keys()
  for sentence_id in sentence_ids:
    silver = silver_data.get(sentence_id, set())
    unsup = unsup_data.get(sentence_id, set())
    if sentence_disagreement(silver, unsup):
      disagreement_sentence_ids.append(sentence_id)

  return disagreement_sentence_ids

def subsample_data(data, keep_proportion, keep_quantity, seed):
  n = len(data)
  if keep_quantity:
    n_keep = keep_quantity
  else:
    n_keep = math.ceil(n * keep_proportion)

  random.seed(seed)
  keep_idx = random.sample(range(n), n_keep)

  sample = [d for i, d in enumerate(data) if i in keep_idx]

  assert len(sample) == n_keep

  return sample

def generate_file_name(base_file, seed, keep_amount):
  return base_file.split('.txt')[0] + f'_keep{keep_amount}_seed{seed}' + '.txt'

def write_output(output_file, data):
  sentence_strs = ['-DOCSTART- -X- -X- O'] + ['\n'.join(sentence_data) for sentence_data in data]

  print(f'Writing data to {output_file}')  
  with open(output_file, "w", encoding="utf-8") as f:
    for sentence_str in sentence_strs:
      f.write(sentence_str)
      f.write('\n\n')

def main():
  args = parse_args()
  if not args.keep_proportion and not args.keep_quantity:
    raise ValueError('Must specify one of keep-proportion and keep-quantity')

  gold_data = load_data(args.gold)
  silver_data = load_data(args.silver)
  unsup_data = load_data(args.unsup)

  assert len(gold_data) == len(silver_data)
  assert len(gold_data) == len(unsup_data)
  
  disagreement_sentence_ids = get_disagreement_sentence_ids(silver_data, unsup_data)

  samples = []
  for seed in args.seeds:
    sample = subsample_data(disagreement_sentence_ids, args.keep_proportion, args.keep_quantity, seed)
    samples.append(sample)

  # For each disagreement sentence id, overwrite that sentence's annotations in the silver data with the values from the gold data
  outputs = []
  for sample in samples:
    output = []
    for i, _ in enumerate(silver_data):
      if i in sample:
        output.append(gold_data[i])
      else:
        output.append(silver_data[i])
    outputs.append(output)

  # Write out modified data to file
  for seed, output in zip(args.seeds, outputs):
    keep_amount = args.keep_proportion or args.keep_quantity
    outfile = generate_file_name(args.gold, seed, keep_amount)
    write_output(outfile, output)

if __name__ == "__main__":
  main()
