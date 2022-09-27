f_labs = open("data/gale_en_zh/orig/dev.en.ner")
f_toks = open("data/gale_en_zh/orig/dev.en")
lang = 'en'
print("-DOCSTART- -X- -X- O")
print()
for l, t in zip(f_labs, f_toks):
  l = l.strip()
  t = t.strip()
  l_toks = l.split(" ")
  t_toks = t.split(" ")
  assert(len(l_toks) == len(t_toks))
  for i in range(len(l_toks)):
#    print(t_toks[i]+" "+"DUM"+" "+"DUM"+" "+l_toks[i])
    #wikiann format
    print(lang + ":"+t_toks[i]+"\t"+l_toks[i])
  print()

