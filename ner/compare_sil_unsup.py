import collections
import csv

f_sil = open("data/proj_zh_a-ali-g-txt_test-g/sil.dev.csv")
#line,src_span_toks,tgt_span_toks,src_span_start,src_span_end,tgt_span_start,tgt_span_end,entity

f_uns = open("data/csv/r11.unsup.dev.csv")
f_gol = open("data/csv/gold.dev.csv")

f_sil_reader = csv.reader(f_sil)
f_uns_reader = csv.reader(f_uns)
f_gol_reader = csv.reader(f_gol)

sil_dict = {}
for rows in f_sil_reader:
  if rows[0] in sil_dict:
    sil_dict[rows[0]].append(rows[1:7])
  else:
    sil_dict[rows[0]] = [rows[1:7]]

gol_dict = {}
for rows in f_gol_reader:
  if rows[0] in gol_dict:
    gol_dict[rows[0]].append(rows[1:7])
  else:
    gol_dict[rows[0]] = [rows[1:7]]

uns_dict = {}
for rows in f_uns_reader:
  if rows[0] in uns_dict:
    uns_dict[rows[0]].append(rows[1:7])
  else:
    uns_dict[rows[0]] = [rows[1:7]]

def get_overlap(s1, s2):
    s1 = s1.split()
    s2 = s2.split()
    multiset_1 = collections.Counter(s1)
    multiset_2 = collections.Counter(s2)
    overlap = list((multiset_1 & multiset_2).elements())
    return " ".join(overlap)

f_semisup = open("semisup.csv", 'w')
semisup_writer = csv.writer(f_semisup)
fieldnames = ["line","src_span_toks","tgt_span_toks","src_span_start","src_span_end","tgt_span_start","tgt_span_end"]
semisup_writer.writerow(fieldnames)
for sil_l, sils in sil_dict.items():
  if sil_l in uns_dict.keys():
    unsups = uns_dict[sil_l]
    for sil in sils:
      src_span_toks = sil[0]
      tgt_span_toks = sil[1]
      src_span_start = sil[2]
      src_span_end = sil[3]
      tgt_span_start = sil[4]
      tgt_span_end = sil[5]
      #print(src_span_toks,tgt_span_toks,src_span_start,src_span_end,tgt_span_start,tgt_span_end)
      for unsup in unsups:
        if src_span_start == unsup[2] and src_span_end == unsup[3]:
          assert(src_span_toks == unsup[0])
          overlap_st = get_overlap(tgt_span_toks, unsup[1])
          lg = len(overlap_st)
          if lg>0 and max(len(tgt_span_toks), len(unsup[1]))*0.3<=lg: 
            #print("overlap", sil)
            sil1 = sil
            sil1.insert(0,sil_l)
            if overlap_st == tgt_span_toks: # same
               print("yes same")
            else:
               print("yes overlap")
            semisup_writer.writerow(sil1)
          else:
            # replace with gold
            gols = gol_dict[sil_l]
            for gol in gols:
              if src_span_start == gol[2] and src_span_end == gol[3]:
                assert(src_span_toks == gol[0])
                #print("no overlap, replace with", gol)
                gol1= gol
                gol1.insert(0, sil_l) 
                print("no overlap", gol1)
                semisup_writer.writerow(gol1)
            
  else:
    #print("no such line in unsupervised data", sil_l)  
    # replace with gold
    if sil_l in gol_dict.keys():
      gols = gol_dict[sil_l]
      for gol in gols:
        gol1= gol
        gol1.insert(0, sil_l) 
        print("no overlap, not in unsup", gol1)
        semisup_writer.writerow(gol1)
