# Chase Checking

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func
from calendar_months import months_dict 


def keyword_search(test, extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            if i + 2 < len(lines):
                if test:
                    print(f"TEST: returning keyword_search: {lines[i+2]}")
                return lines[i+2]
    return None


def find_month(test, extracted_text):
    keyphrase = 'Columbus, OH 43218 - 2051'
    return_text = keyword_search(test, extracted_text, keyphrase)
    return_text_split = return_text.split(' ')
    var_month, var_year = return_text_split[-3], return_text_split[-1]
    for i, month in months_dict.items():
        if var_month == month: # Redundant check of successful scrape
            if test:
                print(f"TEST: returning month {i}: {month}")
            return f"{var_month} {var_year}", return_text
    return None


def find_ending_balance(test, extracted_text):
    keyphrase = "Ending Balance\n"
    print(f"keyphrase: {keyphrase}")
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase == line.strip():
            print(f"{find_ending_balance}: {i}, {line}")


def main(test, extracted_text):
    # Collecting CSV headers
    stmt_essential_keys = ['month', 'period', 'balance',]
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    stmt_essential_dict['month'], stmt_essential_dict['period'] = find_month(test, extracted_text)
    stmt_essential_dict['balance'] = find_ending_balance(test, extracted_text)


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240320-statements-9266-.pdf'
    with open(path, 'r', encoding="utf-8", errors="replace") as file:
        extracted_text = extraction_func(path)
    main(test, extracted_text)


'''
Commit Comments:
- 

'''