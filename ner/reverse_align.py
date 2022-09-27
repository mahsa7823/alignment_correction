f = open("data/gale_en_zh/orig/train.aln")
for l in f:
  l = l.strip()
  aligns = l.split(" ")
  rev = ''
  for align in aligns:
    align_sides = align.split("-")
    rev += align_sides[1]+"-"+align_sides[0] + " "
  print(rev.strip())
