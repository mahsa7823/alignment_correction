gold_f = open("data/gale_en_zh/gold_zh/test.txt")
silver_f = open("data/gale_en_zh/proj_zh_a-ali-g-txt_test-c/test.txt")
unsup_f = open("data/gale_en_zh/proj_zh_unsup_test-c/test.txt")

for gol, sil, uns in zip(gold_f, silver_f,unsup_f):
  sil = sil.strip()
  uns = uns.strip()
  gol = gol.strip()
  gol_cols = gol.split(" ")
  sil_cols = sil.split(" ")
  uns_cols = uns.split(" ")
  if len(gol_cols) > 1: 
    print(gol_cols[3])
#    if sil_cols[3] != uns_cols[3]:
#      print(gol)
#      if gol_cols[3] != 'O':
#        print("DIFF")
#    else:
#      #print(sil_cols[0]+" "+sil_cols[1]+" "+sil_cols[2]+" "+_cols[3])
#      print(sil)
#  else:
#    print()

