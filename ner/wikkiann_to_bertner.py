f = open("data/gale_en_zh/proj_zh_a-ali-g-txt_test-g/train/train")
print("-DOCSTART- -X- -X- O")
print()
for l in f:
  l = l.strip()
  tok_tag = l.split("\t")
  if len(tok_tag) == 2:
    print(tok_tag[0][2:]+" DUM DUM "+ tok_tag[1])
  else:
    print()
