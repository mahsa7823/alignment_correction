import json
import pandas as pd
from argparse import ArgumentParser
import collections


def get_overlap(s1, s2):
    s1 = s1.split()
    s2 = s2.split()
    multiset_1 = collections.Counter(s1)
    multiset_2 = collections.Counter(s2)
    overlap = list((multiset_1 & multiset_2).elements())
    return " ".join(overlap)


p = ArgumentParser()
p.add_argument("-d", "--silver", help="path to silver json file", default="silver.analysis-eventBased.json")
p.add_argument("-u", "--unsup", help="path to output file of the unsupervised method",
               default="new_outputs/bet-analysis.diffsum.intersection.json")
p.add_argument("-i", "--gold", help="path to gold extractions", default="analysis-gold-event.mid")
p.add_argument("-o", "--out", help="path to output file", default="test.out")
opts = p.parse_args()

gold = {}
with open(opts.silver) as f:
    silver = json.load(f)

with open(opts.unsup) as tfp, open(opts.gold) as afp:
    for i, inf in zip(tfp.readlines(), afp.readlines()):
        i = json.loads(i)
        inf = json.loads(inf)
        gold[inf["id"]] = {}
        temp = []
        src_tgt = []
        event_ids = []
        types = []
        for ii in range(len(inf["source_spans"])):
            bound = inf["source_spans"][ii]
            text = " ".join((inf["source"][bound[0]:bound[1] + 1]))
            temp.append((text, inf["span_ids"][ii], inf["event_ids"][ii], inf["ent_names"][ii], bound))
            src_tgt.append((" ".join((inf["source"])), " ".join(inf["target"])))
            event_ids.append(inf["source"])

        gold[inf["id"]]["source_id_tup"] = temp
        gold[inf["id"]]["src_tgt"] = src_tgt
        gold[inf["id"]]["source_spans"] = []
        gold[inf["id"]]["target_spans"] = []
        gold[inf["id"]]["span_id"] = []
        gold[inf["id"]]["event_id"] = []
        gold[inf["id"]]["ent_names"] = []
        for ii in i["alignment"]:
            gold[inf["id"]]["source_spans"].append(" ".join(ii["source_span_tokens"]))
            gold[inf["id"]]["target_spans"].append(" ".join(ii["target_span_tokens"]))
            gold[inf["id"]]["span_id"].append(ii["s_id"])
            gold[inf["id"]]["event_id"].append(ii["e_id"])
            gold[inf["id"]]["ent_names"].append(ii["e_name"])

count_spans = 0
empty_silver = 0
empty_unsupervised = 0
same = 0
overlap = 0

dict = {'doc_id': [], 'event_id': [], 'ann_type': [], 'ss-id': [], 'source_sent': [], 'target_sent': [],
        'source_span': [], 'silver_span': [],
        'unsupervised_span': [], 'src_token_start_end': []}
output = open("out.txt", "w")
output.write("Source\t\tUnsupervised\t\tSilver\n")
for i in gold.keys():
    line = ""
    for j in range(len(gold[i]["source_id_tup"])):
        g_text = ""
        id_s = gold[i]["source_id_tup"][j][1]
        id_e = gold[i]["source_id_tup"][j][2]
        ann = gold[i]["source_id_tup"][j][3]
        indx = gold[i]["source_id_tup"][j][4]
        source_text = gold[i]["source_id_tup"][j][0]
        count_spans += 1
        line += source_text + '\t\t'
        dict['ss-id'].append(id_s)
        dict['doc_id'].append(i)
        dict['event_id'].append(id_e)
        dict['ann_type'].append(ann)
        dict['src_token_start_end'].append(indx)
        src = gold[i]["src_tgt"][j][0]
        tgt = gold[i]["src_tgt"][j][1]
        dict['source_sent'].append(src)
        dict['target_sent'].append(tgt)
        dict['source_span'].append(source_text)

        if id_e in gold[i]["event_id"]:
            indices = [k for k, x in enumerate(gold[i]["event_id"]) if x == id_e]
            for k in indices:
                if gold[i]['span_id'][k] == id_s and gold[i]["ent_names"][k] == ann:
                    gold_ind = k
                    line += gold[i]["target_spans"][k] + '\t\t'
                    g_text = gold[i]["target_spans"][k].rstrip()
                    dict['unsupervised_span'].append(g_text)
                    break
                elif k == indices[-1]:
                    empty_unsupervised += 1
                    line += "-\t\t"
                    dict['unsupervised_span'].append(None)
        else:
            dict['unsupervised_span'].append(None)
        if i in silver.keys() and id_e in silver[i]["event_ids"]:
            indices = [k for k, x in enumerate(silver[i]["event_ids"]) if x == id_e]
            for k in indices:
                if silver[i]['span_ids'][k] == id_s and silver[i]["ent_names"][k] == ann:
                    silver_ind = k
                    line += silver[i]["target_spans"][silver_ind] + '\n'
                    s_text = silver[i]["target_spans"][silver_ind].rstrip()
                    dict['silver_span'].append(s_text)
                    if s_text == g_text and s_text != "":
                        same += 1
                    elif s_text != "" and g_text != "" and len(get_overlap(s_text, g_text)) > 0:
                        overlap_st = get_overlap(s_text, g_text).rstrip()
                        lg = len(overlap_st)
                        if lg > 0:
                            if max(len(s_text), len(g_text)) * 0.3 <= lg:
                                overlap += 1

                    break
                elif k == indices[-1]:
                    empty_silver += 1
                    line += "-\n"
                    dict['silver_span'].append(None)

        else:
            dict['silver_span'].append(None)
            empty_silver += 1

    output.write(line)

df = pd.DataFrame.from_dict(dict)
df.to_csv(opts.out, index=False, header=True, encoding="utf-8-sig")

print("all spans:  " + str(count_spans))
print("empty silver:  " + str(empty_silver))
print("empty unsupervised:  " + str(empty_unsupervised))
print("same span:  " + str(same))
print("overlap:  " + str(overlap))
