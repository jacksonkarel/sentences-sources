import argparse

import spacy
from spacy.pipeline import SentenceRecognizer
import jsonlines

my_parser = argparse.ArgumentParser(description='List the content of a folder')

my_parser.add_argument('Text_file',
                       metavar='text',
                       type=str,
                       help='text file input')
my_parser.add_argument('Link',
                       metavar='link',
                       type=str,
                       help='link to document')
my_parser.add_argument('Jsonl_file',
                       metavar='jsonl',
                       type=str,
                       help='jsonl file output')

args = my_parser.parse_args()

text_path = args.Text_file

text_open = open(text_path, "r")
text = text_open.read()
model = "en_core_web_trf"
nlp = spacy.load(model, disable=["ner", "textcat"])
senter = SentenceRecognizer(nlp.vocab, model)
doc = nlp(text)
text_sents = [sent.text for sent in doc.sents]

link = args.Link
jsonl_path = args.Jsonl_file
with jsonlines.open(jsonl_path, mode='w') as writer:
    for sent in doc.sents:
        sent_link = {"text": sent.text, "link": link}
        writer.write(sent_link)