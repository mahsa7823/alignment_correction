import argparse
import math
import random

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--annotation-file', required=True)
  parser.add_argument('--keep-proportion', required=True, type=float, help='proportion of data to keep (between 0 and 1)')
  parser.add_argument('--seeds', required=True, nargs='+', type=int, help='list of seeds')

  args = parser.parse_args()

  return args

def load_data(annotation_file):
  rows = []
  with open(annotation_file, "r", encoding="utf-8") as f:
    for row in f:
      rows.append(row)
  header = rows[0]
  data = rows[1:]
  return header, data

def subsample_data(data, keep_proportion, seed):
  n = len(data)
  n_keep = math.ceil(n * keep_proportion)

  random.seed(seed)
  keep_idx = random.sample(range(n), n_keep)

  sample = [d for i, d in enumerate(data) if i in keep_idx]

  assert len(sample) == n_keep

  return sample

def generate_file_name(base_file, seed, keep_proportion):
  return base_file.split('.csv')[0] + f'.keep{keep_proportion}_seed{seed}' + '.csv'

def write_sample(output_file, sample):
  with open(output_file, "w", encoding="utf-8") as f:
    for row in sample:
      f.write(row)

def main():
  args = parse_args()
  header, data = load_data(args.annotation_file)

  samples = []
  for seed in args.seeds:
    sample = subsample_data(data, args.keep_proportion, seed)
    samples.append(sample)

  for seed, sample in zip(args.seeds, samples):
    outfile = generate_file_name(args.annotation_file, seed, args.keep_proportion)
    sample = [header] + sample
    write_sample(outfile, sample)

if __name__ == "__main__":
  main()
