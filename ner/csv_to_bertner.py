import csv

f_labs_en = open("data/gale_en_zh/orig/train.en.ner")
f_labs_zh = open("data/gale_en_zh/orig/train.zh.ner")
f_toks_zh = open("data/gale_en_zh/orig/train.zh")
f_csv = open("ner_sb/unsup_outputs/r11.unsup.train.csv") # proj_zh_unsup_test-c
#f_csv = open("semisup") # proj_zh_semisup_test-c
#line,src_span_toks,tgt_span_toks,src_span_start,src_span_end,tgt_span_start,tgt_span_end

f_csv_reader = csv.reader(f_csv)
mydict = {}
for rows in f_csv_reader:
  if rows[0] in mydict:
    mydict[rows[0]].append(rows[1:7])
  else:
    mydict[rows[0]] = [rows[1:7]]

line_labels = []
i = 0
for l in f_labs_en:
  labs = l.strip().split(" ")
  ind_lab = {}
  for ind, lab in enumerate(labs):
    ind_lab[ind] = lab
  line_labels.append(ind_lab)
f_labs_en.close()

print("-DOCSTART- -X- -X- O")
print()
l = 0
for toks_zh, labs_zh in zip(f_toks_zh, f_labs_zh):
  if str(l) in mydict.keys():
    csv_info = mydict[str(l)]
#    print("csv_info, toks_zh, labs_zh", csv_info, toks_zh, labs_zh)
    new_labs = []
    for i in range(len(toks_zh.strip().split(" "))):
      new_labs.append("O")
#    print("new_labs", new_labs)
    for info in csv_info:
      #print("info", info) 
      src_span_toks = info[0]
      tgt_span_toks = info[1]
      src_span_start = int(info[2])
      src_span_end = int(info[3])
      src_labs = set()
      for k in range(src_span_start, src_span_end+1):
        src_labs.add(line_labels[l][k][2:]) # remove B- or I-
      assert(len(src_labs) == 1)
      src_lab = src_labs.pop()
#      print("src_lab", src_lab)
      tgt_span_start = int(info[4])
      tgt_span_end = int(info[5])
      for j in range(tgt_span_start, tgt_span_end+1):
        if j == tgt_span_start:
          new_labs[j] = "B-"+src_lab
        else:
          new_labs[j] = "I-"+src_lab
#    print("new_labs", new_labs)
#    print("labs_en", line_labels[l])
    toks_zh_split = toks_zh.strip().split(" ")
    assert(len(toks_zh_split) == len(new_labs))
    for i in range(len(toks_zh_split)):
      print(toks_zh_split[i]+" "+"DUM"+" "+"DUM"+" "+new_labs[i])
  else:
    for i in range(len(toks_zh.strip().split(" "))):
      toks_zh_split = toks_zh.strip().split(" ")
      print(toks_zh_split[i]+" "+"DUM"+" "+"DUM"+" O")
  print()  
  l = l + 1 

