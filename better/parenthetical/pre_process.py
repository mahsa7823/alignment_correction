import json
import csv
import pandas as pd

#f = open("/exp/mmohammadi/better/data/basic_event/gold/clean_sent/basic.eng-provided-72.0pct.train-70.0pct.d.bp.json")
f = open("/exp/mmohammadi/better/data/basic_event/gold/clean_sent/basic.eng-provided-72.0pct.analysis-15.0pct.ref.d.bp.json")
data = json.load(f)
entries = data['entries']

dict = {'sta': [], 'end': [], 'src': []}
for entry_id, entry in entries.items():
  print(entry_id)
  seg_txt_tok = entry['segment-text-tok'][:]
  events = entry['annotation-sets']['basic-events']
  starts_ends = set()
  for span_set_id, span_set in events['span-sets'].items():
    spans = span_set['spans']
    for span in spans:
      sta = span['start-token']
      end = span['end-token']
      starts_ends.add(str(sta) + " "+ str(end))
  
  for sta_end in sorted(starts_ends):
    sta = int(sta_end.split(" ")[0])
    end  = int(sta_end.split(" ")[1])
    seg_txt_tok.insert(end+1, '}')
    seg_txt_tok.insert(sta, '{')
    dict['sta'].append(sta)
    dict['end'].append(end)
    dict['src'].append(' '.join(seg_txt_tok))
    seg_txt_tok = entry['segment-text-tok'][:]

df = pd.DataFrame.from_dict(dict)
df.to_csv("sta_end_src.csv", index=False, header=True, encoding="utf-8")

