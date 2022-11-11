import pandas as pd
from argparse import ArgumentParser
import json

'''
def find_sub_list(sub, l):
    res = []
    for ind in (i for i, e in enumerate(l) if e == sub[0]):
        if l[ind:ind + len(sub)] == sub:
            res.append((ind, ind + len(sub) - 1))

    return res
'''


def overlap(li, ind):
    for i in li:
        if i[0] <= ind[1] and i[1] >= ind[0]:
            return True
    return False


def write_tokens(tokens):
    line = ""
    for i in tokens:
        if i == "\"":
            i = "\'"
        line += "\"\"" + i + "\"\", "
    line = line.rstrip()[0:-2]
    line = line + "\"]\",\""
    return line


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument("-d", "--data", help="path to csv file", default="fa.analysis.csv")
    p.add_argument("-o", "--out", help="path to output file", default="outt")
    opts = p.parse_args()

    df = pd.read_csv(opts.data)

    df_grouped = df.groupby('doc_id')
    out_file = open(opts.out, "w")
    out_file.write("\"src_tokens\",\"tar_tokens\",\"config_obj\"\n")

    # iterate over each group
    for group_name, df_group in df_grouped:
        source_span = df_group['source_span'].tolist()
        silver_span = df_group['silver_span'].tolist()
        unsup_span = df_group['unsupervised_span'].tolist()
        src_sent = df_group['source_sent'].tolist()[0]
        tgt_sent = df_group['target_sent'].tolist()[0]
        src_tokens = src_sent.split()
        tgt_tokens = tgt_sent.split()
        start_end = df_group['src_token_start_end'].tolist()
        indexes = []
        # import pdb; pdb.set_trace();
        for i in range(len(source_span)):
            if silver_span[i] != unsup_span[i]:
                source_span_tokens = source_span[i].split()
                indexes.append((json.loads(start_end[i])[0], json.loads(start_end[i])[1]))

        indexes = list(set(indexes))
        final = [[]]
        for i in range(len(indexes)):
            if i == 0:
                final[0].append(indexes[i])
            else:
                added = False
                for j in final:
                    if not overlap(j, indexes[i]):
                        j.append(indexes[i])
                        added = True
                        break
                if not added:
                    final.append([indexes[i]])

        if final != [[]]:
            counter_h = 0
            # import pdb; pdb. set_trace();
            for i in final:
                counter_h = 0
                i.sort()
                middle = False
                new_tokens = []
                new_indexes = []
                for j in range(len(src_tokens)):
                    if (len(i) > 0) and i[0][0] == i[0][1] and j == i[0][0]:
                        new_tokens.append(src_tokens[j])
                        new_indexes.append(counter_h)
                        counter_h += 1
                        del i[0]
                    elif (len(i) > 0) and (i[0][0] < j <= i[0][1]):
                        new_tokens[-1] = new_tokens[-1] + ' ' + src_tokens[j]
                        if j == i[0][1]:
                            del i[0]
                            new_indexes.append(counter_h - 1)
                    else:
                        new_tokens.append(src_tokens[j])
                        counter_h += 1
            line = "\"["
            line += write_tokens(new_tokens)
            line += "["
            line += write_tokens(tgt_tokens)
            line += "{\"\"src_enable_retokenize\"\": true, \"\"version\"\": {\"\"PATCH\"\": 0, \"\"MAJOR\"\": 1, " \
                    "\"\"MINOR\"\": 0}, \"\"tar_enable_retokenize\"\": false,\"\"src_head_inds\"\":"
            line += str(new_indexes)
            line += "}\""
            out_file.write(line + '\n')
        '''
        else:
            new_tokens = src_tokens
            line = "\"["
            line += write_tokens(new_tokens)
            line += "["
            line += write_tokens(tgt_tokens)
            line += "{\"\"src_enable_retokenize\"\": true, \"\"version\"\": {\"\"PATCH\"\": 0, \"\"MAJOR\"\": 1, " \
                    "\"\"MINOR\"\": 0}, \"\"tar_enable_retokenize\"\": false,\"\"src_head_inds\"\":[]}\""
            out_file.write(line+"\n")
        '''
    out_file.close()
