import starwrap as sw
import numpy as np
import pandas as pd
import re
from nltk.tokenize.toktok import ToktokTokenizer

arg = sw.args()
arg.trainMode = 0

sp = sw.starSpace(arg)

#sp.initFromSavedModel('scientificn1')
sp.initFromTsv('sci-mc5-tm5.tsv')

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


df = pd.read_csv("full_docs.csv")
df.fillna('',inplace=True)

tt = ToktokTokenizer()
df['train_data'] = df['text'].apply(tokenize, args=(tt,))


embeddings = [np.array( sp.getDocVector(doc, ' ') )[0] for doc in df.train_data.values.tolist()]
embeddings = np.array(embeddings)

with open('embed.npy', 'wb') as f:
    np.save(f, embeddings)


