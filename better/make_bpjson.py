import csv
import json
from collections import OrderedDict

new_objs = {}


cmp_res = open("compare.csv", "r", encoding="utf-8-sig")
compare_result = csv.DictReader(cmp_res, delimiter=',')
dict_from_csv = list(compare_result)
for row in dict_from_csv:
  new_obj_dict = {"event_id": '',"ann_type": '',"ss-id": '',"source_span": '',
 "silver_span":'',"sup_span": '',"sup_span_start_tok":'',
 "sup_span_end_tok": '',"sup_span_start": '',"sup_span_end":''}
  #print("row", row)
  new_obj_dict['event_id'] = row['event_id']
  new_obj_dict['ann_type'] = row['ann_type']
  new_obj_dict['ss-id'] = row['ss-id']
  new_obj_dict['source_span'] = row['source_span']
  new_obj_dict['silver_span'] = row['silver_span']
  new_obj_dict['sup_span'] = row['sup_span']
  new_obj_dict['sup_span_tok'] = row['sup_span_tok']
  #sup_span_tok = row['sup_span_tok']
  new_obj_dict['sup_span_start_tok'] = row['sup_span_start_tok']
  new_obj_dict['sup_span_end_tok'] = row['sup_span_end_tok']
  new_obj_dict['sup_span_start'] = row['sup_span_start']
  new_obj_dict['sup_span_end'] = row['sup_span_end']
  new_obj_dict['src_token_start_end'] = row['src_token_start_end']

  if row['doc_id'] in new_objs:
    new_objs[row['doc_id']].append(new_obj_dict)
  else:
    new_objs[row['doc_id']] = [new_obj_dict]
#print("new_obj", new_obj)

with open('data/p1-analysis-silverv4.2.no-filter.bp.json', 'r') as input_file:
#with open('data/p1-train-silverv4.2.no-filter.bp.json', 'r') as input_file:
  input_data = input_file.read()
  # read json file with keeping the order of objects
  data = json.loads(input_data, object_pairs_hook=OrderedDict)

  entries = data['entries']
  #print("old entries", entries)

  for entry_k, entry in entries.items():

    if entry_k in new_objs:
        
        for new_obj in new_objs[entry_k]:
          #if (new_obj['silver_span'] == ''):
          #  if new_obj['ss-id'] in entry['annotation-sets']['basic-events']['span-sets'].keys():
          #    print("SILVER SPAN EMPTY", entry_k, new_obj['ss-id'])
          #  else:
          #    print("This should not happen with 'no-filter' input.", entry_k, new_obj['ss-id'])
          #else:
            for span in  entry['annotation-sets']['basic-events']['span-sets']:
              if span == new_obj['ss-id']:
                span_to_replce = entry['annotation-sets']['basic-events']['span-sets'][span]
                span_dict = span_to_replce['spans']
                for s in span_dict:
                  #print("s['string']", s['string'])
                  #print("new_obj['silver_span']", new_obj['silver_span'])
                  src_span_sta_tok = int(new_obj['src_token_start_end'].strip('][').split(',')[0])
                  src_span_end_tok = int(new_obj['src_token_start_end'].strip('][').split(',')[1])
                  print("DO COMPARISONS")
                  print("s['string']", s['string'])
                  print("new_obj['silver_span']", new_obj['silver_span'])
                  print(src_span_sta_tok, s['start-token'])
                  print(src_span_end_tok, s['end-token'])
                  print("new_obj['sup_span']", new_obj['sup_span'])
                  if (src_span_sta_tok == s['start-token'] and src_span_end_tok == s['end-token']):
                      if (new_obj['silver_span'] == new_obj['sup_span']):
                        print('silver and sup are equal', new_obj['silver_span'])
                      else:
                        print('silver and sup are NOT equal, sup_span:', new_obj['sup_span'], " silver_span:", new_obj['silver_span'])
                      print("REPLACED", entry_k, "span", span, new_obj['sup_span'])
                      #print("s['string'].split(' ')", s['string'].split(' '))
                      s['string'] = new_obj['sup_span']
                      #if ('hstring' not in s or ('hstring' in s and s['hstring'] == '')):
                      #  s['hstring'] = s['string']
                      s['start'] = int(new_obj['sup_span_start'])
                      s['end'] = int(new_obj['sup_span_end'])
                      #s['start-token'] = int(new_obj['sup_span_start_tok'])
                      #s['end-token'] = int(new_obj['sup_span_end_tok'])
                      # change hstring to make sure it is always a substr of string
                      s['hstring'] = s['string']
                      s['hstart'] = s['start']
                      s['hend'] = s['end']
                  else:
                    # half-space cases, or
                    # missing corresponding silver in multi-span cases. e.g.
                    # "9ec7922a-6966-57ec-938f-b2e4c113f48c+4 ss-12 آزادیش ,   لول"
                    # b2a2f1d9-cfde-5ada-bff4-4d7377e6f440+11 ss-8 همسرش ,   نجیب
                    print("***NO REPLACE", entry_k, "span", span, "old: ", s['string'], "\t new:", new_obj['silver_span']) 
                    pass
                #print("after replacement", span_to_replce)

  #print("new entries", entries)
  with open("semi_supervised_toedit.bp.json", 'w', encoding='utf8') as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False)





