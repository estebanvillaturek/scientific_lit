import json
import os
import pandas as pd

RECORD_SEPARATOR = "0x1E" # The good ol' times https://stackoverflow.com/a/41555511/12322720

# Works for authors, keywords and other lists in elsevier json
def process_list(elem_list):
    if not isinstance(elem_list, list):
        elem_list = [elem_list]
    return RECORD_SEPARATOR.join( [elem.get('$','') for elem in elem_list] )

basepath = "data/"
records = []
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            with open(entry, "r") as file:
                raw = json.loads(file.read())
                meta = raw['coredata']
                doc = {}
                doc['text'] = raw.get('originalText','')
                doc['abstract'] = meta.get('dc:description','')
                doc['title'] = meta.get('dc:title','')
                doc['doi'] = meta.get('prism:doi','')
                doc['pubname'] = meta.get('prism:publicationName','')
                doc['pubtype'] = meta.get('pubType','')
                doc['authors'] = process_list(meta.get('dc:creator',[]))
                doc['keywords'] = process_list(meta.get('dcterms:subject',[]))
                records.append(doc)

df = pd.DataFrame(records)
df.to_csv('full_docs.csv',index=False)
