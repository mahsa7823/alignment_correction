import csv
import json
import collections
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
    print("*sup", sup)
    if unsup == sup:
      if unsup == '':
        print("identical empty")
        #pass
      else:
      	print("identical non-empty")
        #pass
    else:
      overlap_st = get_overlap(unsup, sup).rstrip()
      lg = len(overlap_st)
      if lg>0:
        if max(len(unsup), len(sup))*0.3<=lg:
          #overlap
          #pass
          print("yes overlap")
        else:
          #no overlap
          #if sup != '':
           #if (unsup != '' and sup != ''):
           print("no overlap")
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
           print("no overlap")
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
# write output to 'compare.jsonl'

#    if silver != sup and unsup != sup:
#    	overlap_s = get_overlap(silver, sup).rstrip()
#    	overlap_u = get_overlap(unsup, sup).rstrip()
#    	if len(overlap_s) == 0 and len(overlap_u) == 0:
#    		#print(row)
#    		pass
#    	else:
#    		if (max(len(unsup), len(sup))*0.3<=len(overlap_u)
#    			and max(len(silver), len(sup))*0.3<=len(overlap_s)):
#    		  pass
#    		else:
#    		  # no overlap
#    		  print(row)

df = pd.DataFrame.from_dict(dict)
df.to_csv("compare.csv", index=False, header=True, encoding="utf-8-sig")
