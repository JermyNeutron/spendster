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


# Centralized keyword scraping function.
def keyword_search(test, hints_enabled, extracted_text, keyphrase):
    lines = extracted_text
    for i, line in enumerate(lines):
        if keyphrase in line:
            if i + 1 < len(lines):
                if hints_enabled:
                    print(f"HINT: Returning keyword_search: {lines[i+1]}")
                return lines[i+1]
    return None


# Find statement's month.
def find_month(test, hints_enabled, extracted_text):
    keyphrase = 'Columbus, OH 43218 - 2051'
    return_text = keyword_search(test, hints_enabled, extracted_text, keyphrase)
    return_text_split = return_text.split(' ')
    var_month, var_year = return_text_split[-3], return_text_split[-1]
    for i, month in months_dict.items():
        if var_month == month: # Redundant check of successful scrape
            if hints_enabled:
                print(f"HINT: Returning month {{{i}}}: {month}")
            return f"{var_month} {var_year}", return_text
    return None


# Collect statement ending balance.
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
                print(f"HINT: Returning balance: {line}")
            return line.strip()


# Centralized scraping function.
def transaction_scrape(test, hints_enabled, extracted_text, counter, end_phrase):
    date_format = re.compile(r'^\d{2}/\d{2}$')
    transactions_arr = []
    for i in range(0, len(extracted_text) + 1):
        if i == counter:
            j = counter - 1
            while j < len(extracted_text):
                if j + 3 < len(extracted_text):
                    if extracted_text[j].strip() != end_phrase:
                        # If [j] is a misc line to be skipped
                        if not date_format.match(extracted_text[j].strip()):
                            j += 1
                            continue
                        else:
                            trx_date = extracted_text[j].strip()
                            pre_trx_merchant = extracted_text[j + 1].strip()
                            trx_merchant = ' '.join(pre_trx_merchant.split())
                            trx_amount = extracted_text[j + 2].strip()
                            transaction_ind = (trx_date, trx_merchant, trx_amount)
                            transactions_arr.append(transaction_ind)
                            if hints_enabled:
                                print(f"HINT: {trx_date}, {trx_merchant}, {trx_amount}")
                            j += 4
                    else:
                        if hints_enabled:
                            print(f"HINT: Ending phrase met: {j - 1}: \"{extracted_text[j]}\"")
                        return transactions_arr
    return transactions_arr


# Collect first page transactions.
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
        print('\nHINT:', find_starting_transactions)
        print(f"HINT: Transactions start: {counter}")
    return transaction_scrape(test, hints_enabled, extracted_text, counter, end_phrase)


# Determine if second page transactions exist.
def is_adl(test, hints_enabled, extracted_text):
    sp_ind = "*start*transaction detail"
    sp_bool = False
    sp_ind_occurence = []
    for i, line in enumerate(extracted_text, start=1):
        if sp_ind == line:
            sp_ind_occurence.append(i)
    if len(sp_ind_occurence) >= 2:
        if hints_enabled:
            print('\nHINT: ', is_adl)
            for i in sp_ind_occurence:
                print(f"HINT: \"{sp_ind}\" found at {i}")
        sp_bool = True
        sp_counter = sp_ind_occurence.pop() + 7
        return sp_bool, sp_counter
    return sp_bool


# Scrape second page's transactions.
def find_adl_transactions(test, hints_enabled, extracted_text, sp_counter):
    end_phrase = '*end*transaction detail'
    if hints_enabled:
        print('\nHINT:', find_adl_transactions)
        print(f"HINT: Second page counter starts: {sp_counter}")
    return transaction_scrape(test, hints_enabled, extracted_text, sp_counter, end_phrase)


# Pack and write organized data in to CSV.
def create_csv(test, hints_enabled, export_text):
    path = 'temp/temp.csv' if not test else 'temp/test_temp.csv'
    with open(path, mode='w', newline='') as file: # writes CSV
        writer = csv.writer(file)
        writer.writerows(export_text)
        if hints_enabled:
            print('\nHINT: CSV created.')
    with open(path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        formatted_data = '\n'.join('\t'.join(row) for row in csv_data)
        pyperclip.copy(formatted_data)
        print("CSV content has been copied to clipboard. You can now paste it using CTRL+V.")
    if test: # converts type list into string to write into .txt
        csv_view = 'temp/test_csv_view.txt'
        with open(csv_view, 'w') as file:
            for item in export_text:
                file.write(f"{str(item)}\n")
        if hints_enabled:
            print('HINT: CSV view created...')


# Main function of script.
def main(test: bool, hints_enabled: bool, extracted_text: str, stmt_essential_keys=stmt_essential_keys):
    # Collecting CSV headers
    path = 'temp/test_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    extracted_text = [item for item in extracted_text.split('\n') if item != ''] # Chase Checking text requires .split('\n)
    if hints_enabled:
        print('\nHINT:', main)
        print(F"HINT: Statement CSV headers")
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    stmt_essential_dict['month'], stmt_essential_dict['period'] = find_month(test, hints_enabled, extracted_text)
    stmt_essential_dict['balance'] = find_ending_balance(test, hints_enabled, extracted_text)
    transaction_arr: list[str] = find_starting_transactions(test, hints_enabled, extracted_text)
    adl_exit, sp_counter = is_adl(test, hints_enabled, extracted_text)
    if adl_exit:
        transaction_arr.extend(find_adl_transactions(test, hints_enabled, extracted_text, sp_counter))
    create_csv(test, hints_enabled, transaction_arr)


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