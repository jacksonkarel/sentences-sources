import os
import re

import spacy
import jsonlines
# from kaggle.api.kaggle_api_extended import KaggleApi

from helpers import remove_blanks, pdf_text, ebook_text

class Text_to_jsonl:
    def __init__(self, input_path, output, link, cite, gpu):
        self.input_path = input_path
        self.jsonl_file = output
        self.link = link
        self.cite = cite
        self.gpu = gpu
        # self.save_kaggle = kaggle
    
    def dir_file_check(self):
        if os.path.isfile(self.input_path):
            self.filetype_extract(self.input_path)
        elif os.path.isdir(self.input_path):
            for file in os.scandir(self.input_path):
                self.filetype_extract(file)

    def filetype_extract(self, file):
        if file.endswith(".txt"):
            entry_open = open(file, 'r')
            entry_read = entry_open.read()
            format_entry = remove_blanks(entry_read)

        elif file.endswith(".pdf"):
            format_entry = pdf_text(file)

        elif file.endswith(".epub") or file.endswith(".mobi"):
            format_entry = ebook_text(file)
        
        self.sentence_segment(format_entry)

    def sentence_segment(self, text):
        if self.gpu:
            spacy.require_gpu()
        nlp = spacy.load("en_core_web_lg", exclude=["ner", "parser", "tagger", "lemmatizer"])
        nlp.enable_pipe("senter")
        doc = nlp(text)
        text_sents = [sent.text.replace('\n', '') for sent in doc.sents]
        with jsonlines.open(self.jsonl_file, mode='a') as writer:
            for sent_text in text_sents:
                sent_link = {"text": sent_text, "link": self.link}
                if self.cite is not None:
                    sent_link["cite"] = self.cite
                writer.write(sent_link)
        # if self.save_kaggle:
        #     KaggleApi.authenticate()
        #     KaggleApi.datasets_create_version_by_id