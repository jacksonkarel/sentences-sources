import sys

from pdfminer.high_level import extract_text
from epy import get_ebook_obj, parse_html

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

def ebook_text(filepath):
    ebook = get_ebook_obj(filepath)
    try:
        try:
            ebook.initialize()
        except Exception as e:
            sys.exit("ERROR: Badly-structured ebook.\n" + str(e))
        text = ""
        for i in ebook.contents:
            content = ebook.get_raw_text(i)
            src_lines = parse_html(content)
            for j in src_lines:
                line = j + "\n"
                text = "".join((text, line))
        
    finally:
        ebook.cleanup()
    return text