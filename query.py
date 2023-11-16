#!/usr/bin/env python3
# https://www.ncbi.nlm.nih.gov/books/NBK179288/#chapter6.Python_Integration

import sys
import os
import shutil
import edirect

xtract_path = shutil.which('xtract')

if xtract_path is not None:
    sys.path.insert(1, os.path.dirname(xtract_path))
else:
    print("xtract not found in the PATH.")

# for more information regarding the query see the guide: https://dataguide.nlm.nih.gov/edirect/xtract.html
# or watch the webinar videos on YouTube: https://www.youtube.com/playlist?list=PL7dF9e2qSW0a6zx-yGMJvY6mcwQz_Vx4b

query = 'esearch -db pubmed -query ""1533-4406"[JOUR] AND "N Engl J Med"[JOUR]" | \
    efetch -format xml | \
    xtract -set Set -rec Rec -pattern PubmedArticle \
    -if MedlineTA -equals "N Engl J Med" \
    -or NlmUniqueID -equals 0255562 \
    -or ISSNLinking -equals 0028-4793 \
    -or ISSNLinking -equals 1533-4406 \
    -tab "\n" -sep "," \
    -wrp PMID -element MedlineCitation/PMID'

print("Query is being processed..")
results = edirect.pipeline(query)

if results:
    print(results)
else:
    print("No results available.")