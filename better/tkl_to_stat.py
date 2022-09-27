import csv
import json
import pandas as pd

#csv_result = open("data/analysis-Batch_43_results.csv", "r", encoding="utf-8")
csv_result = open("data/train-Batch_results.csv", "r", encoding="utf-8")
#csv_result = open("tmp", "r", encoding="utf-8")
reader = csv.DictReader(csv_result, delimiter=',')

dict = {'doc_id': [], 'event_id': [], 'ann_type': [], 'ss-id': [], 'source_sent': [],
        'target_sent': [],
        'source_span': [], 'sup_span': [], 'sup_span_tok': [], 'sup_span_start_tok': [],'sup_span_end_tok': [], 
        'sup_span_start': [],'sup_span_end': []}

for row in reader:
  #print(row)
  accept_time = row['AcceptTime']
  sumit_time = row['SubmitTime']
  time_sec = row['WorkTimeInSeconds']
  inp_conf_oj = json.loads(row['Input.config_obj'])
  inp_src_tokens = json.loads(row['Input.src_tokens'])
  inp_tar_tokens = json.loads(row['Input.tar_tokens'])
  answer_align = json.loads(row['Answer.alignment'])
  #print(len(inp_src_tokens), len(inp_tar_tokens), len(answer_align))
  assert(len(inp_src_tokens) == len(answer_align))
  src_head_inds = inp_conf_oj['src_head_inds']
  for h in src_head_inds:
    dict['doc_id'].append('')
    dict['event_id'].append('')
    dict['ann_type'].append('')
    dict['ss-id'].append('')
    print("h", h)
    dict['source_sent'].append(" ".join(inp_src_tokens))
    print(" ".join(inp_src_tokens))
    dict['target_sent'].append(" ".join(inp_tar_tokens))
    print(" ".join(inp_tar_tokens))
    dict['source_span'].append(inp_src_tokens[h])
    print(inp_src_tokens[h])
    #print(h, inp_src_tokens[h], answer_align[h])
    sup_tar_span = ''
    sup_tar_span_tok = []
    sup_span_idx = []
    for i, a in enumerate(answer_align[h]):
      if a == True:
        sup_tar_span += inp_tar_tokens[i] + ' '
        sup_span_idx.append(i)
        sup_tar_span_tok.append(inp_tar_tokens[i])
    dict['sup_span'].append(sup_tar_span.strip())
    dict['sup_span_tok'].append(sup_tar_span_tok)
    if (len(sup_span_idx) > 0):
      dict['sup_span_start_tok'].append(sup_span_idx[0]) # start token
      dict['sup_span_end_tok'].append(sup_span_idx[-1]) # end token
      start = 0
      end = 0
      leng = 0
      for l in range(sup_span_idx[0], sup_span_idx[-1]+1):
        leng += len(inp_tar_tokens[l]) + 1
      leng -= 1
      for l in range(sup_span_idx[0]):
        start += len(inp_tar_tokens[l]) + 1
        #print("inp_tar_tokens[l], start", inp_tar_tokens[l], start)
      end = start + leng
      dict['sup_span_start'].append(start)
      dict['sup_span_end'].append(end)
    else:
      dict['sup_span_start_tok'].append(0)
      dict['sup_span_end_tok'].append(0)
      dict['sup_span_start'].append(0)
      dict['sup_span_end'].append(0)
    print(sup_tar_span.strip())
  print()
print("dict", dict)

df = pd.DataFrame.from_dict(dict)
df.to_csv("sup_span.csv", index=False, header=True, encoding="utf-8-sig")
