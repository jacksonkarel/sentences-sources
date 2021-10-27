def remove_blanks(data) :
    entry_list = data.split('\n')
    for line in entry_list:
        if line == '':
            entry_list.remove(line)
    no_b_str = '\n'.join(entry_list)
    return no_b_str  