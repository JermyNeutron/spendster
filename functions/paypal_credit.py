# PayPal Credit

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func, extraction_writing
from functions.calendar_months import months_dict # preceding '.' for main.py execution


def keyphrase_ambig_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> int:
    occurences = []
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            occurences.append(i)
    if hints_enabled:
        print('\nHINT:', keyphrase_search)
        print('HINT:', occurences)
    return occurences

def keyphrase_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> int:
    occurences = []
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase == line.strip():
            occurences.append(i)
    if hints_enabled:
        print('\nHINT:', keyphrase_search)
        print('HINT:', occurences)
    return occurences


def find_month(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'Statement Closing Date:'
    counter = keyphrase_ambig_search(hints_enabled, extracted_text, keyphrase)[0] # Expect single counter    
    for i, line in enumerate(extracted_text, start=1):
        if i == counter:
            sel_line = line
            break
    sel_line = sel_line.replace(keyphrase, '').strip()
    var_month = sel_line.split(' ')[-1].split('/')[0]
    var_year = sel_line.split(' ')[-1].split('/')[-1]
    for i, month in months_dict.items():
        if int(var_month) == i:
            hints_enabled and print(f"HINT: Returning statement month {{{i}}}: {month} 20{var_year}")
            return f'{month} 20{var_year}'
        

def find_balance(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'New Balance'
    counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)[0]
    for i, line in enumerate(extracted_text, start=1):
        if i == counter:
            hints_enabled and print('HINT: returning statement balance:', extracted_text[i])
            return extracted_text[i]
        

def find_minimum(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'Minimum Payment Due'
    counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)[0]
    for i, line in enumerate(extracted_text, start=1):
        if i == counter:
            hints_enabled and print('HINT: returning statement minimum due:', extracted_text[i])
            return extracted_text[i]


def find_transactions(hints_enabled: bool, extracted_text: list) -> list:
    keyphrase = '\nDescription\nAmount'
    end_phrase = 'Total Purchases & Adjustments'
    skip_phrase = 'No Interest If Paid In Full'
    transactions_arr = []
    path = 'temp/test_temp_scrape.txt'
    with open(path, 'r', encoding='utf-8', errors='replace') as file:
        uf_text = file.read()
        index = 0
        line_number = 1
        occurences = []
        while index != -1:
            index = uf_text.find(keyphrase, index)
            if index != -1:
                line_number = uf_text[:index].count('\n')
                line_number += 1
                occurences.append(line_number)
                index += len(keyphrase)
    print(occurences)
    # counter = occurences[-1]
    # for i, line in enumerate(extracted_text, start=1):
    #     if i == counter:
    #         j = i + 2
    #         while j < len(extracted_text):
    #             if j + 6 < len(extracted_text):
    #                 if end_phrase in extracted_text[j]:
    #                     if hints_enabled:
    #                         print('\nHINT:', find_transactions)
    #                         print('HINT: transactions',transactions_arr)
    #                     return transactions_arr
    #                 else:
    #                     trx_date = extracted_text[j].strip()
    #                     trx_merchant = extracted_text[j+4].strip()
    #                     if skip_phrase in extracted_text[j+5]:
    #                         trx_amount = extracted_text[j+6].strip()
    #                         trx_ind = (trx_date, trx_amount, trx_merchant)
    #                         transactions_arr.append(trx_ind)
    #                         j+=7
    #                     else:
    #                         trx_amount = extracted_text[j+5].strip()
    #                         trx_ind = (trx_date, trx_amount, trx_merchant)
    #                         transactions_arr.append(trx_ind)
    #                         j+=6


# Unpack stmt_essential_dict items into CSV.
def unpack_dict(hints_enabled: bool, stmt_essential_dict: dict) -> list:
    keyval_par = []
    for key, value in stmt_essential_dict.items():
        keyval_par.append((key, value))
    if hints_enabled:
        print('\nHINT:', unpack_dict)
        for i in keyval_par:
            print('HINT: unpacking', i)
    print()
    return keyval_par


def create_csv(test: bool, hints_enabled: bool, export_data: list) -> None:
    path = 'temp/temp.csv' if not test else 'temp/test_temp.csv'
    with open(path, mode='w', newline='') as file: # writes CSV
        writer = csv.writer(file)
        writer.writerows(export_data)
        hints_enabled and print('\nHINT: CSV created.')
    with open(path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        formatted_data = '\n'.join('\t'.join(row) for row in csv_data)
        pyperclip.copy(formatted_data) # copies CSV into clipboard
        print("CSV content has been copied to clipboard. You can now paste it using CTRL+V")
    if test:
        csv_view = 'temp/test_csv_view.txt'
        with open(csv_view, 'w') as file:
            for item in export_data:
                file.write(f"{str(item)}\n")
        hints_enabled and print('\nHINT: CSV view created...')


def main(test: bool, hints_enabled: bool, extracted_text: list) -> None:
    export_data = []
    stmt_essential_keys = ['month', 'balance', 'payment']
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    stmt_essential_dict['month'] = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['balance'] = find_balance(hints_enabled, extracted_text)
    stmt_essential_dict['payment'] = find_minimum(hints_enabled, extracted_text)
    export_data.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    find_transactions(hints_enabled, extracted_text)
    # export_data.extend(find_transactions(hints_enabled, extracted_text))
    # create_csv(test, hints_enabled, export_data)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/paypal_05.pdf'
    uf_text = extraction_func(path)
    extraction_writing(test, uf_text)
    extracted_text = [item.strip() for item in uf_text.split('\n') if item != '']
    # for item in extracted_text:
    #     re.sub(r'\s+', ' ', item)

    main(test, hints_enabled, extracted_text)