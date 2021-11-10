import re

def preprocess(file):
    with open(file) as f:
        read_text = f.read()

    
    remove_pg_nums = re.sub("\n+\s*\d+\n", "\n", read_text)
    remove_caps_titles = re.sub("\n\s*[A-Z]([A-Z]|\s|:|\?)*\n", "\n", remove_pg_nums)


    with open(file, 'w') as f:
        f.write(remove_caps_titles)
