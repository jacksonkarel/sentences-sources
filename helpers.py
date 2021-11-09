import re
import os

from pdfminer.high_level import extract_text

def remove_blanks(data):
    entry_list = data.split('\n')
    for line in entry_list:
        if line == '':
            entry_list.remove(line)
    no_b_str = '\n'.join(entry_list)
    return no_b_str  

def pdf_text(file):
    text = extract_text(file)
    format_entry = remove_blanks(text)
    return format_entry

def ebook_text(file):
    sub_exten = re.sub("\.(?!.*\.).*", ".txt", file)
    sub_space = re.sub(" ", "_", sub_exten)
    epy_cmd = f"epy -d {file} > {sub_space}"
    os.system(epy_cmd)
    entry_open = open(sub_space, 'r')
    entry_read = entry_open.read()
    format_entry = remove_blanks(entry_read)                
    rm_cmd = f"rm {sub_space}"
    os.system(rm_cmd)
    return format_entry