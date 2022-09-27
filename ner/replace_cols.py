f = open("../../BERT-NER/data/train.txt")

for l in f:
  l = l.strip().split(" ")
  if len(l) == 4:
    print(l[0]+" "+"DUM"+" "+"DUM"+" "+l[3])
  else:
    print()

