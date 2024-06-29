# PayPal Credit

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func_pypdf2, extraction_writing
from functions.calendar_months import months_dict # preceding '.' for main.py execution


def stmt_essential_extrap(uf_str: str, keyphrase: str) -> str:
    return uf_str.replace(keyphrase, '')


def find_month(hints_enabled: bool, uf_str: str) -> str:
    month_str = uf_str.replace('Payment Due Date: ', '').split('/')
    var_month = month_str[0]
    for key, value in months_dict.items():
        if int(var_month) == key:
            return_month = value
    hints_enabled and print(f'HINT: returning statement month: {return_month} 20{month_str[-1]}')
    return f'{return_month} 20{month_str[-1]}'


def trx_fil(trx_str: str) -> list:
    skip_phrases = ['Standard', 'Deferred', 'No Interest If Paid In Full']
    for i in skip_phrases:
        trx_str = trx_str.replace(i, '')
    return trx_str.split()


def find_transactions(hints_enabled: bool, extracted_text: list) -> list:
    transactions_arr = []
    keyphrase = 'PURCHASES & ADJUSTMENTS'
    end_phrase = 'Total Purchases'
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase == re.sub(r'\s+', ' ', line):
            j = i + 1
            while j < len(extracted_text):
                if end_phrase not in extracted_text[j]:
                    trx_str = trx_fil(extracted_text[j])
                    trx_date = trx_str[0]
                    trx_amount = trx_str[-1]
                    trx_merchant = ' '.join(trx_str[3:-1])
                    trx_ind = [trx_date, trx_amount, trx_merchant]
                    transactions_arr.append(trx_ind)
                    j += 1
                else:
                    if hints_enabled:
                        print('\nHINT:', find_transactions)
                        for i in transactions_arr:
                            print('HINT:', i)
                    return transactions_arr


# Unpack stmt_essential_dict items into CSV.
def unpack_dict(hints_enabled: bool, stmt_essential_dict: dict) -> list:
    keyval_par = []
    for key, value in stmt_essential_dict.items():
        keyval_par.append((key, value))
    if hints_enabled:
        print('\nHINT:', unpack_dict)
        for i in keyval_par:
            print('HINT: unpacking', i)
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
    stmt_essential_dict['month'] = find_month(hints_enabled, extracted_text[-2])
    stmt_essential_dict['balance'] = stmt_essential_extrap(extracted_text[-3], 'New Balance: $')
    stmt_essential_dict['payment'] = stmt_essential_extrap(extracted_text[-1], 'Minimum Payment Due: $')
    export_data.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    export_data.extend(find_transactions(hints_enabled, extracted_text))
    create_csv(test, hints_enabled, export_data)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/paypal_11.pdf'
    uf_text = extraction_func_pypdf2(path)
    extracted_text = [item.strip() for item in uf_text.split('\n') if item != '']
    write_text = ''
    for i, line in enumerate(extracted_text, start=1):
        write_text += f'{i} {line}\n'
    extraction_writing(test, write_text)
    main(test, hints_enabled, extracted_text)