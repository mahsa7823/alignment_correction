import csv
import json
from collections import OrderedDict

cmp_res = open("../span_alignment/compare.csv", "r", encoding="utf-8-sig")
compare_result = csv.DictReader(cmp_res, delimiter=',')
dict_from_csv = list(compare_result)
for row in dict_from_csv:
  docid = row['doc_id']
  ssid = row['ss-id']
  if docid == '27585024-e0af-556a-82d8-b4448fea2ede+1' and ssid == 'ss-5':
    print(row)
  elif docid == 'd05d7bbd-505f-5f2b-8074-5907539a273e+1' and ssid == 'ss-24':
    print(row)
  elif docid == '02cacfd9-7d50-59ac-beb6-d9750e03a574+3' and ssid == 'ss-1':
    print(row)
