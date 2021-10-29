# sentences-sources
Script that segments sentences from text and pairs them with a link in jsonlines
## Instillation
```
pip install -r requirements.txt
```
## Usage
```
usage: sentences_sources.py [-h] [--cite CITE] [--gpu] input jsonl link

positional arguments:
  input        text file input
  jsonl        jsonl file output
  link         link to document

optional arguments:
  -h, --help   show this help message and exit
  --cite CITE  text citation
  --gpu        enable gpu

```
