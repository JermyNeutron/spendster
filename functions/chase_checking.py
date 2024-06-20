# Chase Checking

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func
from calendar_months import months_dict 


# Dictionary keys to return.
stmt_essential_keys = ['month', 'period', 'balance',]


# Transaction class
class Transaction:
    def __init__(self, date, merchant, amount) -> None:
        self.date = date
        self.merchant = merchant
        self.amount = amount

    def __repr__(self) -> str:
        return f"Transaction({{{self.date}}}={self.date}, {{{self.merchant}}}={self.merchant}, {{{self.amount}}}={self.amount})"


def keyword_search(test, hints_enabled, extracted_text, keyphrase):
    lines = extracted_text
    for i, line in enumerate(lines):
        if keyphrase in line:
            if i + 1 < len(lines):
                if hints_enabled:
                    print(f"HINT: returning keyword_search: {lines[i+1]}")
                return lines[i+1]
    return None


def find_month(test, hints_enabled, extracted_text):
    keyphrase = 'Columbus, OH 43218 - 2051'
    return_text = keyword_search(test, hints_enabled, extracted_text, keyphrase)
    return_text_split = return_text.split(' ')
    var_month, var_year = return_text_split[-3], return_text_split[-1]
    for i, month in months_dict.items():
        if var_month == month: # Redundant check of successful scrape
            if hints_enabled:
                print(f"HINT: returning month {{{i}}}: {month}")
            return f"{var_month} {var_year}", return_text
    return None


def find_ending_balance(test, hints_enabled, extracted_text):
    keyphrase = "Ending Balance"
    occurences = []
    # Find line number for keyphrase
    for i, line in enumerate(extracted_text, start=1): #
        if keyphrase == line.strip():
            if hints_enabled:
                print(f"HINT: {find_ending_balance}: {i}, {line.strip()}")
            occurences.append(i)
    # Find next line after keyphrase to return statement ending balance
    counter = occurences.pop(0) + 1
    for i, line in enumerate(extracted_text, start=1): #
        if counter == i:
            if hints_enabled:
                print(f"HINT: returning balance: {line}")
            return line.strip()


def find_starting_transactions(test, hints_enabled, extracted_text):
    keyphrase = "Beginning Balance"
    end_phrase = "*end*transaction detail"
    occurences = []
    # find line number for keyphrase
    for i, line in enumerate(extracted_text, start=1): #
        if keyphrase == line.strip():
            if hints_enabled:
                print(f"HINT: {find_starting_transactions}: {i}, {line.strip()}")
            occurences.append(i)
    counter = occurences.pop() + 2
    if hints_enabled:
        print(f"HINT: transactions start: {counter}")
    for i, line in enumerate(extracted_text, start=1): #
        if counter == i:
            for i in range(counter, len(extracted_text), 3):
                pass
    # Date, Merchant, Transaction
    # +4 to repeat
    # *end*transaction detail stop


def find_adl_transactions(test, hints_enabled, extracted_text):
    # *start*transaction detail, if x2 = 2nd page exists
    # *end*transaction detail stop
    sp_ind = "*start*transaction detail"
    sp_ind_occurence = []
    for i, line in enumerate(extracted_text, start=1):
        if sp_ind == line:
            sp_ind_occurence.append(i)
    if len(sp_ind_occurence) <= 2:
        sp_counter = sp_ind_occurence.pop()
    if hints_enabled:
        print(f"HINT: Second Page counter starts: {sp_counter+7}")


def main(test, hints_enabled, extracted_text, stmt_essential_keys=stmt_essential_keys):
    # Collecting CSV headers
    path = 'temp/test_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    extracted_text = [item for item in extracted_text.split('\n') if item != ''] # Chase Checking text requires .split('\n)
    with open(path, 'w', encoding='utf-8', errors='replace') as file: # removable
        for item in extracted_text:
            file.write(f"{str(item)}\n")
    if hints_enabled:
        print(F"HINT: statement CSV headers")
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    stmt_essential_dict['month'], stmt_essential_dict['period'] = find_month(test, hints_enabled, extracted_text)
    stmt_essential_dict['balance'] = find_ending_balance(test, hints_enabled, extracted_text)
    find_starting_transactions(test, hints_enabled, extracted_text)
    find_adl_transactions(test, hints_enabled, extracted_text)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/20240320-statements-9266-.pdf'
    with open(path, 'r', encoding="utf-8", errors="replace") as file:
        extracted_text = extraction_func(path)
    main(test, hints_enabled, extracted_text)


'''
Commit Comments:
- 

'''