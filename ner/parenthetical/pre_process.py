import re
sents=[]
labs=[]
M="test"
def convert_bio_to_spans(bio_sequence):
    spans = []  # (label, startindex, endindex)
    cur_start = None
    cur_label = None
    N = len(bio_sequence)
    for t in range(N + 1):
        if (cur_start is not None) and (t == N or re.search("^[BO]", bio_sequence[t])):
            assert cur_label is not None
            spans.append((cur_label, cur_start, t))
            cur_start = None
            cur_label = None
        if t == N:
            continue
        assert bio_sequence[t] and bio_sequence[t][0] in ("B", "I", "O")
        if bio_sequence[t].startswith("B"):
            cur_start = t
            cur_label = re.sub("^B-?", "", bio_sequence[t]).strip()
        if bio_sequence[t].startswith("I"):
            if cur_start is None:
                # warning(
                #     "BIO inconsistency: I without starting B. Rewriting to B.")
                newseq = bio_sequence[:]
                newseq[t] = "B" + newseq[t][1:]
                return convert_bio_to_spans(newseq)
            continuation_label = re.sub("^I-?", "", bio_sequence[t])
            if continuation_label != cur_label:
                newseq = bio_sequence[:]
                newseq[t] = "B" + newseq[t][1:]
                # warning(
                #     "BIO inconsistency: %s but current label is '%s'. Rewriting to %s"
                #     % (bio_sequence[t], cur_label, newseq[t]))
                return convert_bio_to_spans(newseq)

    # should have exited for last span ending at end by now
    assert cur_start is None
    return spans




with open("/export/fs04/a07/shabnam/BERT-NER/data/gale_en_zh/orig/"+M+".en","r") as inp:
    for line in inp:
        line=line.rstrip()
        sents.append(line.split())
with open("/export/fs04/a07/shabnam/BERT-NER/data/gale_en_zh/orig/"+M+".en.ner","r") as inp:
    for line in inp:
        line=line.rstrip()
        labs.append(line.split())

new_sents=[]
sent_ids=[]
all_labs= []
for i in range(len(labs)):
    no_lab=True
    all_spans = convert_bio_to_spans(labs[i])
    if len(all_spans)==0:
        new_sents.append(sents[i])
        sent_ids.append(i)
    else:
        #import pdb;pdb.set_trace();
        for jj in all_spans:
            copy_sents = sents[i][:]
            new_sents.append(copy_sents)
            sent_ids.append(i)
            new_sents[-1].insert(jj[1],"{")
            new_sents[-1].insert(jj[2]+1,"}")
            all_labs.append(jj[0])

with open(M+".en.par","w") as out:
    for i in new_sents:
        out.write(" ".join(i)+"\n")

with open(M+".en.par.ids","w") as out:
    for i in sent_ids:
        out.write(str(i)+"\n")
with open(M+".en.par.labs","w") as out:
    for i in all_labs:
        out.write(i+"\n")

    #import pdb; pdb.set_trace()
    #print("hi")


