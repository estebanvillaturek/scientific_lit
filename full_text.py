from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
from elsapy.elssearch import ElsSearch
import json

## Load configuration
con_file = open("config.json")
client = json.load(con_file)
con_file.close()

GET_ALL = False # False gets one chunk (25) True gets all or max (5000)
FULLTEXT = False # Save fulltext
OPENACCESS = True # Search only openaccess documents (so we can get the full text)

query = "public policy"

if OPENACCESS:
  query = "openaccess(1) AND " + query

doc_srch = ElsSearch(query,'sciencedirect')
doc_srch.execute(client, get_all = GET_ALL)

print ("# Found", len(doc_srch.results), "results.")

for doc in doc_srch.results:
  doi = doc['dc:identifier']
  print( doi )
  if FULLTEXT:
    ## ScienceDirect (full-text) document example using DOI
    doi_doc = FullDoc(doi = doi)
    if doi_doc.read(client):
        doi_doc.write() 
    else:
        print ("Read full-text failed for DOI" ,doi)