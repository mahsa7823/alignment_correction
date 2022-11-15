import csv
import json
import collections
import sys
import pandas as pd

def get_overlap(s1, s2):
    s1 = s1.split()
    s2 = s2.split()
    multiset_1 = collections.Counter(s1)
    multiset_2 = collections.Counter(s2)
    overlap = list((multiset_1 & multiset_2).elements())
    return " ".join(overlap)

#dict = {'doc_id': [], 'event_id': [], 'ann_type': [], 'ss-id': [], 'source_sent': [],
#        'target_sent': [],'source_span': [], 'nsupervised_span,': [],'silver_span': [],
#        'sup_span': [], 'sup_span_start_tok': [],'sup_span_end_tok': [], 
#        'sup_span_start': [],'sup_span_end': []}
dict = {'doc_id': [], 'event_id': [], 'ann_type': [], 'ss-id': [], 'source_span': [], 'silver_span': [],
        'sup_span': [], 'sup_span_tok': [], 'sup_span_start_tok': [],'sup_span_end_tok': [], 
        'sup_span_start': [],'sup_span_end': [], 'src_token_start_end': []}

with open('combine.csv', encoding='utf-8-sig') as csvf:
  csvReader = csv.DictReader(csvf)
  visited_spans = [] 
  n_identical = 0
  n_overlapping = 0
  n_different = 0
  for row in csvReader:
   if row['doc_id']+","+row['ss-id']+","+row['source_span'] not in visited_spans:
    visited_spans.append(row['doc_id']+","+row['ss-id']+","+row['source_span'])
    #print("silver", row['silver_span'])
    silver = row['silver_span'].replace(u"\u200c", " ")
    #print("*silver", silver)
    #print("unsup", row['unsupervised_span'])
    unsup = row['unsupervised_span'].replace(u"\u200c", " ")
    #print("*unsup", unsup)
    #print("sup", row['sup_span'])
    sup = row['sup_span'].replace(u"\u200c", " ")
    #print("*sup", sup)
    if sys.argv[1] == 'silver':
      against = silver
    elif sys.argv[1] == 'unsup':
      against = unsup
    if against == sup:
      if against == '':
        # identical empty
        n_identical += 1
      else:
        # identical non-empty
        n_identical += 1
    else:
      overlap_st = get_overlap(against, sup).rstrip()
      lg = len(overlap_st)
      if lg>0:
        if max(len(against), len(sup))*0.3<=lg:
          # overlapping
          n_overlapping += 1
        else:
          #no overlap
          #if sup != '':
           #if (unsup != '' and sup != ''):
           n_different += 1
           dict['doc_id'].append(row['doc_id'])
           dict['event_id'].append(row['event_id'])
           dict['ann_type'].append(row['ann_type'])
           dict['ss-id'].append(row['ss-id'])
           dict['source_span'].append(row['source_span'])
           dict['silver_span'].append(row['silver_span'])
           dict['sup_span'].append(row['sup_span'])
           dict['sup_span_tok'].append(row['sup_span_tok'])
           dict['sup_span_start_tok'].append(row['sup_span_start_tok'])
           dict['sup_span_end_tok'].append(row['sup_span_end_tok'])
           dict['sup_span_start'].append(row['sup_span_start'])
           dict['sup_span_end'].append(row['sup_span_end'])
           dict['src_token_start_end'].append(row['src_token_start_end'])

           #pass
      else:
      	#no overlap
      	  #if sup != '':
           #if (unsup != '' and sup != ''):
           n_different += 1
           dict['doc_id'].append(row['doc_id'])
           dict['event_id'].append(row['event_id'])
           dict['ann_type'].append(row['ann_type'])
           dict['ss-id'].append(row['ss-id'])
           dict['source_span'].append(row['source_span'])
           dict['silver_span'].append(row['silver_span'])
           dict['sup_span'].append(row['sup_span'])
           dict['sup_span_tok'].append(row['sup_span_tok'])
           dict['sup_span_start_tok'].append(row['sup_span_start_tok'])
           dict['sup_span_end_tok'].append(row['sup_span_end_tok'])
           dict['sup_span_start'].append(row['sup_span_start'])
           dict['sup_span_end'].append(row['sup_span_end'])
           dict['src_token_start_end'].append(row['src_token_start_end'])
  
  print("Identical", n_identical)
  print("Overlapping", n_overlapping)
  print("Different", n_different)
df = pd.DataFrame.from_dict(dict)
df.to_csv("compare.csv", index=False, header=True, encoding="utf-8-sig")
