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
# or watch the webinar on YouTube: https://www.youtube.com/playlist?list=PL7dF9e2qSW0a6zx-yGMJvY6mcwQz_Vx4b

query = 'efetch -db pubmed -id 7254297 -format xml | \
        xtract -set Set -rec Rec -pattern PubmedArticle \
        -if MedlineTA -equals "N Engl J Med" \
        -or NlmUniqueID -equals 0255562 \
        -or ISSNLinking -equals 0028-4793 \
        -or ISSNLinking -equals 1533-4406 \
        -tab "\n" -sep "," \
        -pkg Common \
        -wrp PMID -element MedlineCitation/PMID \
        -wrp Title -element Article/ArticleTitle \
        -wrp Abstract -element Abstract/AbstractText \
        -pkg MeshTermList -wrp MeshTerm -element MeshHeading/DescriptorName'

print(edirect.pipeline(query))