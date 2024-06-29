# Synchrony

import csv
import re
import sys

import pyperclip

sys.path.append('.')

from functions.inst_pars import extraction_func_def, extraction_writing # REMOVABLE
from .calendar_months import months_dict # preceding '.' for main.py execution


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
            return f'{month} {var_year}'
        

def find_balance(hints_enabled: bool, extracted_text: list) -> tuple[str, int]:
    hints_enabled and print('HINT:', find_balance)
    keyphrase = 'Days in Billing Period'
    counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)[0]
    for i, line in enumerate(extracted_text, start=1):
        if i == (counter + 2):
            sel_line = line
            hints_enabled and print(f'HINT: statement balance: {sel_line}')
            return sel_line, counter
        

def find_minimum(hints_enabled: bool, extracted_text: list, min_counter: int) -> str:
    hints_enabled and print('HINT:', find_minimum)
    for i, line in enumerate(extracted_text, start=1):
        if i == (min_counter + 1):
            sel_line = line
            hints_enabled and print(f'HINT: statement minimum due: {sel_line}')
            return sel_line


def find_transactions(hints_enabled: bool, extracted_text: list) -> list:
    hints_enabled and print('HINT:', find_transactions)
    date_format = re.compile(r'^\d{2}/\d{2}/\d{4}$')
    keyphrase = 'Amount'
    transition_phrase = '0000'
    end_phrase = 'Continued on next page'
    transactions_arr = []
    counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)[0] # expect first occurence
    # Collect transactions, set default for amounts
    for i, line in enumerate(extracted_text, start=1):
        if i == counter:
            j = counter + 1
            while j < len(extracted_text):
                if j + 3 < len(extracted_text):
                    if transition_phrase in extracted_text[j] or not date_format.match(
                        extracted_text[j].strip()):
                            tp_i = j # index of starting amount
                            hints_enabled and print('HINT:', transactions_arr)
                            break
                    else:
                        trx_date = extracted_text[j].strip()
                        uf_trx_merchant = extracted_text[j+2].strip()
                        trx_merchant = re.sub(r'\s+', ' ', uf_trx_merchant).strip()
                        trx_amount = int
                        trx_ind = [trx_date, trx_amount, trx_merchant]
                        transactions_arr.append(trx_ind)
                        j += 4
    # Collect amounts
    amount_arr = []
    for i, line in enumerate(extracted_text, start=1):
        if i == tp_i:
            j = i
            while j < len(extracted_text):
                if transition_phrase in extracted_text[j] or end_phrase in extracted_text[j]:
                    hints_enabled and print('HINT:', amount_arr)
                    break
                else:
                    amount_arr.append(extracted_text[j])
                    j+=1
    # Assign amounts to transactions
    for i in range(len(transactions_arr)):
        transactions_arr[i][1] = amount_arr[i]
    hints_enabled and print(f'HINT:', transactions_arr)
    return transactions_arr
    

def unpack_dict(hints_enabled: bool, extracted_text: list, stmt_essential_dict: dict) -> list:
    keyval_par = []
    for key, value in stmt_essential_dict.items():
        keyval_par.append((key, value))
    if hints_enabled:
        print('\nHINT:', unpack_dict)
        for i in keyval_par:
            print(f"HINT: unpacking", i)
    return keyval_par


def create_csv(test: bool, hints_enabled: bool, export_text: list) -> None:
    path = 'temp/temp.csv' if not test else 'temp/test_temp.csv'
    with open(path, mode='w', newline='') as file: # writes CSV
        writer = csv.writer(file)
        writer.writerows(export_text)
        hints_enabled and print('\nHINT: CSV created.')
    with open(path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        formatted_data = '\n'.join('\t'.join(row) for row in csv_data)
        pyperclip.copy(formatted_data) # copies CSV into clipboard
        print("CSV content has been copied to clipboard. You can now paste it using CTRL+V")
    if test:
        csv_view = 'temp/test_csv_view.txt'
        with open(csv_view, 'w') as file:
            for item in export_text:
                file.write(f"{str(item)}\n")
    hints_enabled and print('\nHINT: CSV view created...')


def main(test: bool, hints_enabled: bool, extracted_text: list) -> None:
    export_data = []
    stmt_essential_keys = ['month', 'balance', 'minimum amount due',]
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    stmt_essential_dict['month'] = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['balance'], min_counter = find_balance(hints_enabled, extracted_text)
    stmt_essential_dict['minimum amount due'] = find_minimum(hints_enabled, extracted_text, min_counter)
    transactions_arr = find_transactions(hints_enabled, extracted_text)
    export_data.extend(unpack_dict(hints_enabled, extracted_text, stmt_essential_dict))
    export_data.extend(transactions_arr)
    create_csv(test, hints_enabled, export_data)

if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/synchrony_06.pdf'
    # path = 'rep_statements/synchrony_05.pdf'
    # path = 'rep_statements/synchrony_06.pdf'
    uf_text = extraction_func_def(path)
    extraction_writing(test, uf_text)
    extracted_text = [item.strip() for item in uf_text.split('\n') if item != '']

    main(test, hints_enabled, extracted_text)