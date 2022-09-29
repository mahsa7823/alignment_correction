from operator import itemgetter
import re
M= "train"
def match_span_segment(seg, string):
    cursor = 0
    found = []
    for i, s in enumerate(seg):
        if s == string[cursor]:
            cursor += 1
            if cursor == len(string):
                for x in reversed(range(len(string))):
                    found.append(i - x + 1)
                    # cursor = 0
                break  # find only the first occurence
        else:
            cursor = 0
    return found
tgt_sents = []
ids=[]
labs=[]
tgt_maps={}
count=-1
with open("par/"+M+".en.par.zh.tok", "r") as inp:
    for line in inp:
        tgt_sents.append(line.strip())
with open(M+".en.par.ids", "r") as inp:
    for line in inp:
        line=line.strip()
        ids.append(int(line))
with open(M+".en.par.labs", "r") as inp:
    for line in inp:
        line=line.strip()
        labs.append(line)
src=[]
with open(M+".en.par","r") as inp:
    for line in inp:
        src.append(line.strip())

check=0
for i in range(len(src)):
    if "{" in src[i] and ("{" not in tgt_sents[i] or "}" not in tgt_sents[i]):
            tgt_sents[i]=tgt_sents[i].replace("{","").replace("}","")
            del labs[check]
            continue
    if "{" in tgt_sents[i] and "}" in tgt_sents[i]:
        check+=1

di={}
cc=0
check=0
for i in range(len(tgt_sents)):
    if "{" in tgt_sents[i]:
        check+=1

    if i==0 or ids[i]!=ids[i-1]:
        di[ids[i]]={"tokens":[], "maps":[]}
        sp = tgt_sents[i].split()
        for j in sp:
            if j!="{" and j!= "}":
                di[ids[i]]["tokens"].append(j)
    elif ids[i]==ids[i-1]:
        if tgt_sents[i].replace("{","").replace("}","")!=di[ids[i]]["tokens"]:
            m = re.search('{(.+?)}', tgt_sents[i])
            if m:
                found = m.group(1).strip()
                if len(found.split())==0:
                    cc+=1
                    continue
                offs = match_span_segment(di[ids[i]]["tokens"],found.split())
                if len(offs) ==0:
                    cc+=1
                    continue
                elif len(offs)==1:
                    di[ids[i]]["maps"].append([offs[0]-1,offs[0]-1,labs[cc]])
                    cc+=1
                    continue
                else:
                    di[ids[i]]["maps"].append([offs[0]-1,offs[-1]-1,labs[cc]])
                    cc+=1
                    continue
            else:
                continue

    sp = tgt_sents[i].split()
    st,end=-100,-100
    for j in range(len(sp)):
        if sp[j] == "{":
            st=j
        if sp[j]=="}":
            end=j-2
    if st!=-100:
        di[ids[i]]["maps"].append([st,end,labs[cc]])
        cc+=1
tokens=[]
labs=[]
for i in range(len(di.keys())):
    copy=[]
    dels=[]
    if len(di[i]["maps"])>1:
        di[i]["maps"]=sorted(di[i]["maps"], key=itemgetter(0))
        for j in range(1,len(di[i]["maps"])):
                if di[i]["maps"][j][0]<=di[i]["maps"][j-1][1]:
                    dels.append(j)
        for jj in range(len(di[i]["maps"])):
            if jj not in dels:
                copy.append(di[i]["maps"][jj])
        if len(dels)>0:
            di[i]["maps"]=copy


for i in range(len(di.keys())):
    di[i]["maps"]=sorted(di[i]["maps"], key=itemgetter(0))
    inside = False
    labs.append([])
    for t in range(len(di[i]["tokens"])):
        if len(di[i]["maps"])==0:
            labs[-1].append("O")
        elif t==di[i]["maps"][0][0] and t==di[i]["maps"][0][1]:
            labs[-1].append("B-"+di[i]["maps"][0][2])
            del di[i]["maps"][0]
        elif t==di[i]["maps"][0][0]:
            labs[-1].append("B-"+di[i]["maps"][0][2])
            inside = True
        elif t==di[i]["maps"][0][1]:
            labs[-1].append("I-"+di[i]["maps"][0][2])
            inside =False
            del di[i]["maps"][0]
        elif inside:
            labs[-1].append("I-"+di[i]["maps"][0][2])
        else:
            labs[-1].append("O")

        

print(len(labs))
print(di.keys())
st = "-DOCSTART- -X- -X- O\n"

with open("par/"+M+".22txt","w") as outp:
    outp.write(st)
    for i in range(len(di.keys())):
        outp.write("\n")
        for j in range(len(di[i]["tokens"])):
            outp.write(di[i]["tokens"][j]+" DUM DUM "+labs[i][j]+"\n")

    


        #sp = line.split()
        #(st,end) = (-100,-100)
        #for i in range(len(sp)):
        #    if sp[i]=="{":
        #        st = i+1
        #    if sp[i]=="}"
        #        end=i-1

