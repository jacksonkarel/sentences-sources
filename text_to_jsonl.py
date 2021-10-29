import os
import re

import spacy
import jsonlines
from pdfminer.high_level import extract_text

class Text_to_jsonl:
    def __init__(self, input_path, jsonl_file, link, cite, gpu):
        self.input_path = input_path
        self.jsonl_file = jsonl_file
        self.link = link
        self.cite = cite
        self.gpu = gpu
    
    def dir_file_check(self):
        if os.path.isfile(self.input_path):
            self.filetype_extract(self.input_path)
        elif os.path.isdir(self.input_path):
            for file in os.scandir(self.input_path):
                self.filetype_extract(file)
    def filetype_extract(self, file):
        if file.endswith(".pdf"):
            text = extract_text(file)
            format_entry = self.remove_blanks(text)  

        elif file.endswith(".epub") or file.endswith(".mobi"):
            sub_exten = re.sub("\.(?!.*\.).*", ".txt", file)
            sub_space = re.sub(" ", "_", sub_exten)
            epy_cmd = f"epy -d {file} > {sub_space}"
            os.system(epy_cmd)
            entry_open = open(sub_space, 'r')
            entry_read = entry_open.read()
            format_entry = self.remove_blanks(entry_read)                
            rm_cmd = f"rm {sub_space}"
            os.system(rm_cmd)
        
        elif file.endswith(".txt"):
            entry_open = open(file, 'r')
            entry_read = entry_open.read()
            format_entry = self.remove_blanks(entry_read)
        
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

    def remove_blanks(self, data):
        entry_list = data.split('\n')
        for line in entry_list:
            if line == '':
                entry_list.remove(line)
        no_b_str = '\n'.join(entry_list)
        return no_b_str  