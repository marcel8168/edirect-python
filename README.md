<h1 align="center">
  <br>
   <p>EDirect Python Implementation</p>
  <br>
</h1>
<p align="center">
This repository contains code for querying the PubMed database via NCBI's Entrez Direct (EDirect) using Python. There are also examples of other library functions that can be used for similar queries (but with possible limitations).
</p>

## Table of contents

* [Common usage](#common-usage)
* [Installation](#installation)
* [Further Information](#further-information)
* [License](#licence)

## Common usage
Commonly this is used for querying publications from PubMed. This was implemented for my [master's thesis](https://github.com/marcel8168/medtextclassifier) in order to create a custom dataset for fine-tuning NLP models.

## Installation
```shell
git clone https://github.com/marcel8168/edirect-python .
cd edirect-python
docker compose up
```

## Example Usage
```python
# Extract data from XML and create a DataFrame
xml_file = "nejm_data.xml"
data_path = "../edirect-python/results/"

data = []

tree = ElementTree()
xml = tree.parse(data_path + xml_file)

for rec in xml.findall('.//Rec'):
    try: 
        common = rec.find('.//Common')
        pmid = common.find('PMID').text
        title = common.find('Title').text
        abstract = common.find('Abstract').text
        mesh_term_list = rec.find('.//MeshTermList')
        mesh_terms = [term.text for term in mesh_term_list.findall('MeshTerm')]
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Error occured for PMID: {pmid}")

    data.append({'pmid': pmid, 'title': title,
                'abstract': abstract, 'meshtermlist': mesh_terms, 'label': 0})
df = pd.DataFrame(data)
```

## Further Information
##### EDirect and E-Utilities
|Topic|Link|
|:-----|:--------|
|PubMed API|https://www.ncbi.nlm.nih.gov/pmc/tools/developers/|
|Entrez Direct|https://www.ncbi.nlm.nih.gov/books/NBK179288/|
|EDirect Installation|https://dataguide.nlm.nih.gov/edirect/install.html|
|ESearch|https://dataguide.nlm.nih.gov/edirect/esearch.html|
|Xtract|https://dataguide.nlm.nih.gov/edirect/xtract.html|
|E-Utilities|https://www.ncbi.nlm.nih.gov/books/NBK25499/|
|Journal IDs|https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt|
##### Library Options
|Topic|Link|
|:-----|:--------|
|URL query|https://github.com/dtoddenroth/medicaleponyms/blob/main/downloadabstracts/pubmedcache.py|
|MetaPub|https://github.com/metapub/metapub|
|PyMed|https://github.com/gijswobben/pymed|
|EntrezPy|https://gitlab.com/ncbipy/entrezpy|

## License

[MIT License](LICENSE) (Marcel Hiltner, 2023)
