from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
from elsapy.elssearch import ElsSearch
import json

## Load configuration
config = {}
with open('config.json') as config_file:
  config = json.load(config_file)

GET_ALL = config['get_all'] # False gets one chunk (25) True gets all or max (5000)
FULL_TEXT = config['full_text'] # Save fulltext
OPEN_ACCESS = config['open_access'] # Search only openaccess documents (so we can get the full text)

# "public policy AND (impact OR result OR evaluation OR evidence) AND (climate OR environment)"
query = config['query']

if OPEN_ACCESS:
  query = "openaccess(1) AND " + query

client = ElsClient(config['api_key'])

doc_srch = ElsSearch(query,'sciencedirect')
doc_srch.execute(client, get_all = GET_ALL)

for doc in doc_srch.results:
  doi = doc['dc:identifier']
  print( doi )
  if FULL_TEXT:
    ## ScienceDirect (full-text) document example using DOI
    doi_doc = FullDoc(doi = doi)
    if doi_doc.read(client):
        doi_doc.write() 
    else:
        print ("Read full-text failed for DOI" ,doi)

print ("# Found", len(doc_srch.results), "results.")