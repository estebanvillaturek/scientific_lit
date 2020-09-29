import re
from nltk.tokenize.toktok import ToktokTokenizer
import pandas as pd
import numpy as np

RECORD_SEPARATOR = "0x1E"

def tokenize(text, tt):
    text = " ".join(tt.tokenize(text))
    
    # Adapted from toktok
    PERIOD_AND_SPACE_1 = re.compile(r"(?<!\.)\.\s"), r" . "
    PERIOD_AND_SPACE_2 = re.compile(r"""(?<!\.)\.\s*(["'’»›”]) *\s"""), r" . \1"
    ONE_SPACE = re.compile(r" {2,}"), " "
    RXS = [PERIOD_AND_SPACE_1, PERIOD_AND_SPACE_2, ONE_SPACE]
    
    for regexp, subsitution in RXS:
        text = regexp.sub(subsitution, text)
    
    return text.strip().lower()

def labelize(text):
    LABEL_PREFIX = "__label__"
    NONLETTERS = re.compile(r"""[^a-z]+""")
    return LABEL_PREFIX + NONLETTERS.sub("_", text.strip().lower())


df = pd.read_csv("full_docs.csv")
df.fillna('',inplace=True)

tt = ToktokTokenizer()
df['train_data'] = df['text'].apply(tokenize, args=(tt,))

df['labels'] = df.keywords.apply(lambda x: " ".join( map(labelize, x.split(RECORD_SEPARATOR)) ))
df.labels = df.labels.str.cat(df.pubname.apply(labelize), sep=" ")

df.train_data = df.train_data.str.cat(df.labels, sep=" ")

np.savetxt('train_data.txt', df.train_data, fmt = "%s")
