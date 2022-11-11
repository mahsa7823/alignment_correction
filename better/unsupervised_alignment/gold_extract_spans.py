import json, os
from sacremoses import MosesTokenizer
from argparse import ArgumentParser

mt = MosesTokenizer(lang='en')


def load_data(DATA_FILE, translation_file, task="basic"):
    if not os.path.isfile(DATA_FILE):
        raise FileNotFoundError(f"Could not find {DATA_FILE}")
    if not os.path.isfile(translation_file):
        raise FileNotFoundError(f"Could not find {translation_file}")

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    translations = []
    with open(translation_file, "r") as f:
        for line in f:
            line = line.rstrip()
            line = line.replace("\u200c", " ")
            translations.append(line)

    out = []
    index = 0
    entries = data['entries']
    for entry_k, entry in entries.items():
        segment_text = "TMPLASTWORD " + entry['segment-text'] + " TMPLASTWORD"
        segment_text_tok = mt.tokenize(segment_text)
        text_src = []
        text_tmp = segment_text_tok[1:-1]
        id = entry_k
        for j in text_tmp:
            if j != "\ufeff":
                text_src.append(j)
        text_tgt = translations[index].split()
        annotation_sets = entry['annotation-sets']
        if task == 'abstract':
            events = annotation_sets['abstract-events']
        elif task == 'basic':
            events = annotation_sets['basic-events']
        span_sets = events['span-sets']
        strings_indexes = []
        span_ids = []
        for span_set_k, span_set in span_sets.items():
            spans = span_set['spans']
            for span in spans:
                strings_indexes.append([span['start-token'], span['end-token']])
                span_ids.append(span_set_k)

        ent_string_indexes = []
        event_ids = []
        span_list_ids = []
        names = []
        events = events['events']
        for event_k, event in events.items():
            for ss_id in event['agents']:
                ent_string_indexes.append(strings_indexes[span_ids.index(ss_id)])
                event_ids.append(event_k)
                span_list_ids.append(ss_id)
                names.append('agent')
            for ss_id in event["patients"]:
                ent_string_indexes.append(strings_indexes[span_ids.index(ss_id)])
                event_ids.append(event_k)
                span_list_ids.append(ss_id)
                names.append('patient')
            if event["anchors"]:
                ent_string_indexes.append(strings_indexes[span_ids.index(event["anchors"])])
                event_ids.append(event_k)
                span_list_ids.append(event["anchors"])
                names.append('anchor')

        if len(event_ids)>0:
                out.append({"source": text_src, "target": text_tgt, "source_spans": ent_string_indexes, "target_spans": None, "id": id, "span_ids": span_list_ids, "event_ids": event_ids, "ent_names": names})
        # print(out[-1])
        index += 1

    return out


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument("-d", "--data", help="path to basic tokenized bp.json file")
    p.add_argument("-t", "--translation", help="path to translation file (one line per sentence)")
    p.add_argument("-o", "--out", help="path to output file")
    opts = p.parse_args()

    out = load_data(opts.data, opts.translation, "basic")

    with open(opts.out, "w") as f:
        for i in out:
            f.write(json.dumps(i,ensure_ascii=False) + '\n')

