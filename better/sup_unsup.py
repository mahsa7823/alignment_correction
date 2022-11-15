import csv
import json
import sys
import pandas as pd

if sys.argv[1] == 'analysis':
  unsup_result = open("data/stat.out.analysis", "r", encoding="utf-8-sig")
  wc_unsup = 1148
elif sys.argv[1] == 'train':
  unsup_result = open("data/stat.out.train", "r", encoding="utf-8-sig")
  wc_unsup=5858
unsup_reader = csv.DictReader(unsup_result, delimiter=',')
sup_result = open("sup_span.csv", "r", encoding="utf-8-sig")
sup_reader = csv.DictReader(sup_result, delimiter=',')

dict = {'doc_id': [], 'event_id': [], 'ann_type': [], 'ss-id': [], 'source_sent': [],
        'target_sent': [], 'source_span': [], 'unsupervised_span': [], 'silver_span': [], 'sup_span': [], 'sup_span_tok': [],
        'sup_span_start_tok': [],'sup_span_end_tok': [], 'sup_span_start': [],'sup_span_end': [], 'src_token_start_end': []}

all_unsup = []
for un in unsup_reader:
  all_unsup.append(un)
visit_un = dict.fromkeys(range(wc_unsup),0)
for sup in sup_reader:
  for i, un in enumerate(all_unsup):
  	#print(un)
    if (sup['source_sent'] == un['source_sent'] and 
  	  sup['target_sent'] == un['target_sent'] and 
  	  sup['source_span'] == un['source_span']
      ):
      #if (sup['sup_span'] == ''):
      #  print(i, un) 
      visit_un[i] += 1
  	  #else
      dict['doc_id'].append(un['doc_id'])
      dict['event_id'].append(un['event_id'])
      dict['ann_type'].append(un['ann_type'])
      dict['ss-id'].append(un['ss-id'])
      dict['source_sent'].append(un['source_sent'])
      dict['target_sent'].append(un['target_sent'])
      dict['source_span'].append(un['source_span'])
      dict['silver_span'].append(un['silver_span'])
      dict['unsupervised_span'].append(un['unsupervised_span'])
      dict['sup_span'].append(sup['sup_span'])
      dict['sup_span_tok'].append(sup['sup_span_tok'])
      dict['sup_span_start_tok'].append(sup['sup_span_start_tok'])
      dict['sup_span_end_tok'].append(sup['sup_span_end_tok'])
      dict['sup_span_start'].append(sup['sup_span_start'])
      dict['sup_span_end'].append(sup['sup_span_end'])
      dict['src_token_start_end'].append(un['src_token_start_end'])
for v in visit_un:
  if visit_un[v] == 0:
    if all_unsup[v]['silver_span'] != all_unsup[v]['unsupervised_span']:
      print(v, all_unsup[v])
df = pd.DataFrame.from_dict(dict)
df.to_csv("combine.csv", index=False, header=True, encoding="utf-8-sig")
# RUN THIS:
# sed "s/$(echo -ne '\u200c')/$(echo -ne ' ')/g" combine.csv > combine-nou200.csv
