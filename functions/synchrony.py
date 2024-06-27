# Synchrony

import sys
sys.path.append('.')

from functions.inst_pars import extraction_func, extraction_writing
from calendar_months import months_dict


def keyphrase_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> int:
    occurences = []
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            occurences.append(i)
    if hints_enabled:
        print('\nHINT:', keyphrase_search)
        print('HINT:', occurences)
    return occurences


def find_month(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'Statement Closing Date:'
    counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)[0] # Expect single counter
    for i, line in enumerate(extracted_text, start=1):
        if i == counter:
            sel_line = line
    var_month = sel_line.split(' ')[-1].split('/')[0]
    var_year = sel_line.split(' ')[-1].split('/')[-1]
    for i, month in months_dict.items():
        if int(var_month) == i:
            hints_enabled and print(f"HINT: Returning month {{{i}}}: {month} {var_year}")
            return month, var_year


def main(test: bool, hints_enabled: bool, extracted_text: list) -> None:
    stmt_essential_keys = ['month', 'minimum payment due',]
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    print(stmt_essential_dict)
    find_month(hints_enabled, extracted_text)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/synchrony_03.pdf'
    # path = 'rep_statements/synchrony_05.pdf'
    # path = 'rep_statements/synchrony_06.pdf'
    uf_text = extraction_func(path)
    extraction_writing(test, uf_text)
    extracted_text = [item.strip() for item in uf_text.split('\n') if item != '']

    main(test, hints_enabled, extracted_text)