import argparse
import os

from text_to_jsonl import Text_to_jsonl

ss_parser = argparse.ArgumentParser(description='Segment sentences from a text file and pair them with a link in a jsonlines file')

ss_parser.add_argument('input_path', metavar='input', type=str, help='text file input')
ss_parser.add_argument('jsonl_file', metavar='jsonl', type=str, help='jsonl file output')
ss_parser.add_argument('link', metavar='link', type=str, help='link to document')
ss_parser.add_argument("--cite", help="text citation")
ss_parser.add_argument("--gpu", help="enable gpu")

args = ss_parser.parse_args()

args_dict = vars(args)
cli_ttj = Text_to_jsonl(**args_dict)
cli_ttj.dir_file_check()
