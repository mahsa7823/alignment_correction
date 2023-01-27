import csv
import json
from collections import OrderedDict

cmp_res = open("../span_alignment/compare.csv", "r", encoding="utf-8-sig")
compare_result = csv.DictReader(cmp_res, delimiter=',')
dict_from_csv = list(compare_result)
for row in dict_from_csv:
  docid = row['doc_id']
  ssid = row['ss-id']
  # Analysis
  if docid == '27585024-e0af-556a-82d8-b4448fea2ede+1' and ssid == 'ss-5':
    print(row)
  elif docid == 'd05d7bbd-505f-5f2b-8074-5907539a273e+1' and ssid == 'ss-24':
    print(row)
  # Train
  elif docid == '02cacfd9-7d50-59ac-beb6-d9750e03a574+3' and ssid == 'ss-1':
    print(row)
  elif docid == '02cacfd9-7d50-59ac-beb6-d9750e03a574+13' and ssid == 'ss-50':
    print(row)
  elif docid == '0ba721fe-bdae-5569-927b-3721f533bbc0+0' and ssid == 'ss-9':
    print(row)
  elif docid == '1388473e-8170-50b9-8361-8aeb3c6e6523+6' and ssid == 'ss-2':
    print(row)
  elif docid == '206ea1ce-50ed-56d9-ab4c-b4235a732af8+0' and ssid == 'ss-28':
    print(row)
  elif docid == '2ab255c8-c8b4-52d0-82fe-4151fa7e74f8+1' and ssid == 'ss-12':
    print(row)
  elif docid == '2d037849-5f69-5973-a022-8398433d5a82+3' and ssid == 'ss-1':
    print(row)
  elif docid == '2dbcd20a-372d-5041-9649-c4e906509bbe+12' and ssid == 'ss-44':
    print(row)
  elif docid == '36a4a758-690c-5862-88ba-d290aa108569+0' and ssid == 'ss-3':
    print(row)
  elif docid == '376bd536-b2b9-5b56-9558-0eafcd4e09e0+4' and ssid == 'ss-2':
    print(row)
  elif docid == '376bd536-b2b9-5b56-9558-0eafcd4e09e0+5' and ssid == 'ss-3':
    print(row)
  elif docid == '4dac2187-d4c1-5375-b564-daa0cca80192+11' and ssid == 'ss-29':
    print(row)
  elif docid == '532cdbf5-856b-5151-b9d9-e50f52271ed4+5' and ssid == 'ss-50':
    print(row)
  elif docid == '7b4cfd1f-9f1f-5904-bf93-20b3deec2ef8+0' and ssid == 'ss-1':
    print(row)
  elif docid == '8f89a335-8cfd-59ce-89f8-3a5269dd2c9d+7' and ssid == 'ss-18':
    print(row)
  elif docid == '8f89a335-8cfd-59ce-89f8-3a5269dd2c9d+8' and ssid == 'ss-39':
    print(row)
  elif docid == '97bd1bd4-8a41-51e4-9130-d9b20977a37e+7' and ssid == 'ss-13':
    print(row)
  elif docid == '97bd1bd4-8a41-51e4-9130-d9b20977a37e+9' and ssid == 'ss-40':
    print(row)
  elif docid == '9ca065ad-c8eb-53b6-a8b3-aea777c53d90+8' and ssid == 'ss-23':
    print(row)
  elif docid == 'a482a16c-47cc-5625-ae6e-a6b0718bd098+2' and ssid == 'ss-19':
    print(row)
  elif docid == 'a597d736-3015-53d9-a47d-09ab5187edcc+3' and ssid == 'ss-37':
    print(row)
  elif docid == 'a9ddc7fe-a59b-5b65-a188-3a6e8cada5d6+10' and ssid == 'ss-20':
    print(row)
  elif docid == 'ab221507-2e5e-5eff-b8c5-3ed5d3c3c71f+4' and ssid == 'ss-2':
    print(row)
  elif docid == 'bca478b9-c71b-5026-b974-d05a13ac4e4c+16' and ssid == 'ss-100':
    print(row)
  elif docid == 'bca478b9-c71b-5026-b974-d05a13ac4e4c+16' and ssid == 'ss-56':
    print(row)
  elif docid == 'c1a951c5-c2c8-5a10-b03d-e9751ec98631+1' and ssid == 'ss-28':
    print(row)
  elif docid == 'c1a951c5-c2c8-5a10-b03d-e9751ec98631+8' and ssid == 'ss-18':
    print(row)
  elif docid == 'e5a497bd-7a34-5e7c-910d-8fab2c0cd3bb+8' and ssid == 'ss-5':
    print(row)
  elif docid == 'e6111897-b419-5f66-b95b-2286832670b0+2' and ssid == 'ss-27':
    print(row)
  elif docid == 'eeb788a4-3b63-554a-b05c-c8774bedee61+17' and ssid == 'ss-9':
    print(row)
  elif docid == 'fb88fa3e-b00a-5125-9638-562fe9ee18cc+11' and ssid == 'ss-7':
    print(row)
