# Chase Checking

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func
from calendar_months import months_dict


def find_month(test, extracted_text):
    keyphrase = 'Columbus, OH 43218 - 2051'
    return_month = keyword_search(test, extracted_text, keyphrase)
    return return_month


def keyword_search(test, extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            if i + 2 < len(lines):
                var_month, var_year = lines[i+2].strip().split(sep=' ')[0], lines[i+2].strip().split(sep=' ')[2]
                for i, month in months_dict.items():
                    if month == var_month:
                        var_month = months_dict[i+1]
                        print(f"TEST: returning {var_month} {var_year}")
                        return f"{var_month} {var_year}"

    return None


def main(test):
    pass


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240320-statements-9266-.pdf'
    with open(path, 'r', encoding="utf-8", errors="replace") as file:
        extracted_text = extraction_func(path)
    return_month = find_month(test, extracted_text)
    print(return_month)


'''
Commit Comments:
- 

'''