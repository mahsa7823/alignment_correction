import json, os
from sacremoses import MosesTokenizer
from argparse import ArgumentParser

mt = MosesTokenizer(lang='en')


def load_data(DATA_FILE, task="basic"):
    out = {}
    if not os.path.isfile(DATA_FILE):
        raise FileNotFoundError(f"Could not find {DATA_FILE}")

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    index = 0
    entries = data['entries']
    for entry_k, entry in entries.items():
        text_tgt = entry['segment-text'].replace("\u200c", " ")
        text_tgt = text_tgt.split()
        id = entry_k

        annotation_sets = entry['annotation-sets']
        if task == 'abstract':
            events = annotation_sets['abstract-events']
        elif task == 'basic':
            events = annotation_sets['basic-events']
        strings = []
        span_ids = []
        span_start_end = []
        span_sets = events['span-sets']
        for span_set_k, span_set in span_sets.items():
            spans = span_set['spans']
            for span in spans:
                strings.append(span['string'])
                span_ids.append(span_set_k)
                span_start_end.append((span["start-token"], span["end-token"]))
        ent_strings = []
        event_ids = []
        span_list_ids = []
        names = []
        start_end_token = []
        events = events['events']
        for event_k, event in events.items():
            for ss_id in event['agents']:
                ent_strings.append(strings[span_ids.index(ss_id)])
                start_end_token.append(span_start_end[span_ids.index(ss_id)])
                event_ids.append(event_k)
                span_list_ids.append(ss_id)
                names.append('agent')
            for ss_id in event["patients"]:
                ent_strings.append(strings[span_ids.index(ss_id)])
                start_end_token.append(span_start_end[span_ids.index(ss_id)])
                event_ids.append(event_k)
                span_list_ids.append(ss_id)
                names.append('patient')
            if event["anchors"]:
                ent_strings.append(strings[span_ids.index(event["anchors"])])
                start_end_token.append(span_start_end[span_ids.index(event["anchors"])])
                event_ids.append(event_k)
                span_list_ids.append(event["anchors"])
                names.append('anchor')

        out[id] = {"target": text_tgt, "target_spans": ent_strings, "event_ids": event_ids, "ent_names": names,
                   "span_ids": span_list_ids, "target_psspan_start_end": start_end_token}
        index += 1

    return out


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument("-d", "--data", help="path to basic tokenized bp.json file")
    p.add_argument("-o", "--out", help="path to output file")
    opts = p.parse_args()

    out = load_data(opts.data, "basic")

    with open(opts.out, "w") as f:
        f.write(json.dumps(out, indent=2, ensure_ascii=False))
