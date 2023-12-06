#!/usr/bin/env python3
# https://www.ncbi.nlm.nih.gov/books/NBK179288/#chapter6.Python_Integration

import sys
import os
import shutil

import pandas as pd
import edirect
from xml.etree.ElementTree import fromstring, ElementTree


# query constants
# journal abbreviation and ISSN available under https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt
# note that special characters in the query term lead to syntax errors
JOURNAL = "N Engl J Med"
JOURNAL_ISSN = "1533-4406"
TARGET_DIRECTORY = "results/"
OUTPUT_FILE = "nejm_data.xml"


xtract_path = shutil.which('xtract')

if xtract_path is not None:
    sys.path.insert(1, os.path.dirname(xtract_path))
else:
    print("xtract not found in the PATH.")

if not os.path.exists(TARGET_DIRECTORY):
    os.makedirs(TARGET_DIRECTORY)

# for more information regarding the query see the guide: https://dataguide.nlm.nih.gov/edirect/xtract.html
# or watch the webinar videos on YouTube: https://www.youtube.com/playlist?list=PL7dF9e2qSW0a6zx-yGMJvY6mcwQz_Vx4b
query = f'esearch -db pubmed -query ""{JOURNAL_ISSN}"[JOUR] AND "{JOURNAL}"[JOUR]" | \
    efetch -format xml | \
    xtract -set Set \
        -rec Rec -pattern PubmedArticle \
        -if AbstractText \
        -tab "\n" -sep "," \
        -block PubmedArticle -pkg Common \
            -wrp PMID -element MedlineCitation/PMID \
            -wrp Title -element Article/ArticleTitle \
            -wrp Abstract -element AbstractText \
        -block MeshHeadingList -pkg MeshTermList \
            -wrp MeshTerm -element MeshHeading/DescriptorName'

print("Query is being processed..")
res = edirect.pipeline(query)

if not res:
    print("No results available.")
else:
    res_xml = fromstring(res)
    ElementTree(res_xml).write(TARGET_DIRECTORY + OUTPUT_FILE)
    print(f"Query output written into {TARGET_DIRECTORY + OUTPUT_FILE}")
