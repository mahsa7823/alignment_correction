import sys
src=open(sys.argv[1])
tgt=open(sys.argv[2])
for s,t in zip(src,tgt):
  if t.strip() == '':
    print(s.strip()+" ||| "+s.strip().lower())
  else:
    print(s.strip()+" ||| "+t.strip())
