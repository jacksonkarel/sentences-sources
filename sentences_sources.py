import argparse
import os

from text_to_jsonl import Text_to_jsonl
from helpers import pdf_text, ebook_text

ss_parser = argparse.ArgumentParser(description='Segment sentences from a text file and pair them with a link in a jsonlines file')

ss_parser.add_argument('input_path', metavar = "input", help='text file input')
ss_parser.add_argument('output_file', metavar = "output", help='output file')
ss_parser.add_argument('--link', help='link to document')
ss_parser.add_argument("--cite", help="text citation")
ss_parser.add_argument("--gpu", help="enable gpu", action="store_true")
ss_parser.add_argument("--kaggle", help="save new version of jsonl in kaggle", action="store_true")

args = ss_parser.parse_args()

output_file = args.output_file

if output_file.endswith(".jsonl"):
    args_dict = vars(args)
    cli_ttj = Text_to_jsonl(**args_dict)
    cli_ttj.dir_file_check()

elif output_file.endswith(".txt"):
    input_file = args.input_path
    if input_file.endswith(".pdf"):
        format_entry = pdf_text(input_file)

    elif input_file.endswith(".epub") or input_file.endswith(".mobi"):
        format_entry = ebook_text(input_file)
    
    output_open = open(output_file, "w")
    output_open.write(format_entry)
    output_open.close()