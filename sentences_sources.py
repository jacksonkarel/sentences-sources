import argparse
import os
import re

import spacy
from spacy.pipeline import SentenceRecognizer
import jsonlines
import pdfminer
from pdfminer.high_level import extract_text

from remove_blanks import remove_blanks

def filetype_extract(file):
    if file.endswith(".pdf"):
        text = extract_text(file)
        format_text = remove_blanks(text)  
        sentence_segment(format_text)

    elif file.endswith(".epub") or file.endswith(".mobi"):
        sub_exten = re.sub("\.(?!.*\.).*", ".txt", file)
        sub_space = re.sub(" ", "_", sub_exten)
        epy_cmd = f"epy -d {file} > {sub_space}"
        os.system(epy_cmd)
        entry_open = open(sub_space, 'r')
        entry_read = entry_open.read()
        format_entry = remove_blanks(entry_read)                
        rm_cmd = f"rm {sub_space}"
        os.system(rm_cmd)
        sentence_segment(format_entry)
    
    elif file.endswith(".txt"):
        entry_open = open(file, 'r')
        entry_read = entry_open.read()
        format_entry = remove_blanks(entry_read)
        sentence_segment(format_entry)

def sentence_segment(text):
    doc = nlp(text)
    text_sents = [sent.text.replace('\n', '') for sent in doc.sents]

    link = args.Link
    jsonl_path = args.Jsonl_file
    with jsonlines.open(jsonl_path, mode='w') as writer:
        for sent_text in text_sents:
            sent_link = {"text": sent_text, "link": link}
            if citation is not None:
                sent_link["cite"] = citation
            writer.write(sent_link)

ss_parser = argparse.ArgumentParser(description='Segment sentences from a text file and pair them with a link in a jsonlines file')

ss_parser.add_argument('Input_path', metavar='input', type=str, help='text file input')
ss_parser.add_argument('Jsonl_file', metavar='jsonl', type=str, help='jsonl file output')
ss_parser.add_argument('Link', metavar='link', type=str, help='link to document')
ss_parser.add_argument("--cite", help="text citation")


args = ss_parser.parse_args()

input_path = args.Input_path
citation = args.cite

model = "en_core_web_trf"
nlp = spacy.load(model, disable=["ner", "textcat"])
senter = SentenceRecognizer(nlp.vocab, model)

if os.path.isfile(input_path):
    filetype_extract(input_path)
elif os.path.isdir(input_path):
    for file in os.scandir(input_path):
        filetype_extract(file)
