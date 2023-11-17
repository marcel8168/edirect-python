#!/usr/bin/env python3
# https://www.ncbi.nlm.nih.gov/books/NBK179288/#chapter6.Python_Integration

import sys
import os
import shutil
import edirect
from xml.etree.ElementTree import fromstring, ElementTree

xtract_path = shutil.which('xtract')

if xtract_path is not None:
    sys.path.insert(1, os.path.dirname(xtract_path))
else:
    print("xtract not found in the PATH.")

# for more information regarding the query see the guide: https://dataguide.nlm.nih.gov/edirect/xtract.html
# or watch the webinar videos on YouTube: https://www.youtube.com/playlist?list=PL7dF9e2qSW0a6zx-yGMJvY6mcwQz_Vx4b

query = 'esearch -db pubmed -query ""1533-4406"[JOUR] AND "N Engl J Med"[JOUR]" | \
    efetch -format xml | \
    xtract -set Set \
        -rec Rec -pattern PubmedArticle \
        -if MedlineTA -equals "N Engl J Med" \
        -and AbstractText \
        -tab "\n" -sep "," \
        -block PubmedArticle -pkg Common \
            -wrp PMID -element MedlineCitation/PMID \
            -wrp Title -element Article/ArticleTitle \
            -wrp Abstract -element Abstract/AbstractText \
        -block MeshHeadingList -pkg MeshTermList \
            -wrp MeshTerm -element MeshHeading/DescriptorName'

print("Query is being processed..")
res = edirect.pipeline(query)

if res:
    file = 'result1.xml'
    res_xml = fromstring(res)
    ElementTree(res_xml).write(file)
    print(f"Query output written into {file}")
else:
    print("No results available.")
