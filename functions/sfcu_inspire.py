# Schoolsfirst Inspire

import re
import sys
import warnings

sys.path.append('.') # POSSIBLY REMOVABLE

from functions.calendar_months import months_dict
from functions.create_csv import create_csv
from functions.inst_pars import extraction_func_def, extraction_writing # REMOVEABLE
from functions.unpack_dict import unpack_dict


# Return first occurence of keyphrase
def keyphrase_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> str: # Possibly list for multiple pages
    for line_number, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            hints_enabled and print(f"HINT: keyword_search: {line_number} {line}")
            return line_number


def find_month(hints_enabled: bool, extracted_text: list) -> tuple[str, int]:
    date_pattern = re.compile(r'^\d{2}/\d{2}/\d{2}$')
    date_pull: str
    for i, line in enumerate(extracted_text, start=1):
        if date_pattern.match(line):
            counter = i
            date_pull = line
            break
    dp_month = date_pull.split('/')[0]
    dp_year = date_pull.split('/')[2]
    for key, value in months_dict.items():
        if int(dp_month) == key:
            if hints_enabled:
                print("\nHINT:", find_month)
                print(f"HINT: returning statement month: \"{months_dict[key]} {dp_year}\"")
                print(f"HINT: counter set at {counter}")
            return f"{months_dict[key]} {dp_year}", counter
    

def find_amount_due(hints_enabled: bool, extracted_text: list, counter: int) -> str:
    for i, line in enumerate(extracted_text, start=1):
        if i == counter + 3:
            if hints_enabled:
                print('\nHINT:', find_amount_due)
                print(f'HINT: statement amount due: {line}')
            return line


def find_transactions(hints_enabled: bool, extracted_text: list) -> list:
    transactions_arr: list = []
    keyphrase = "Transactions"
    end_phrase = "Fees"
    hints_enabled and print('\nHINT:', find_transactions)
    kp_counter = keyphrase_search(hints_enabled, extracted_text, keyphrase)
    for i in range(1, len(extracted_text) + 1):
        if i == kp_counter:
            j = kp_counter + 6
            while j < len(extracted_text):
                if j + 5 < len(extracted_text):
                    if end_phrase in extracted_text[j]:
                        return transactions_arr
                    else:
                        trx_date = extracted_text[j].strip()
                        uf_trx_merchant = extracted_text[j+3]
                        trx_merchant = re.sub(r'\s+', ' ', uf_trx_merchant).strip()
                        trx_amount = extracted_text[j+5].rstrip('-').strip()
                        trx_ind = (trx_date, trx_amount, trx_merchant)
                        transactions_arr.append(trx_ind)
                        hints_enabled and print(f"HINT: transaction found: {trx_date}, {trx_amount}, {trx_merchant}")
                        j+=6


def main(test: bool, hints_enabled: bool, extracted_text: list) -> None:
    stmt_essential_keys = ['month', 'balance']
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    export_text = []
    stmt_essential_dict['month'], counter = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['balance'] = find_amount_due(hints_enabled, extracted_text, counter)
    fp_trx = find_transactions(hints_enabled, extracted_text)
    export_text.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    export_text.extend(fp_trx)
    create_csv(test, hints_enabled, export_text)


if __name__ == '__main__':
    # Simulated inputs
    test = True
    hints_enabled = True
    template_path = 'rep_statements\sfcu-cc-05.pdf'
    uf_text= extraction_func_def(template_path)
    extraction_writing(test, uf_text)
    path = 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        uff_text = file.read()
    extracted_text = [item.strip() for item in uff_text.split('\n') if item != '']
    main(test, hints_enabled, extracted_text)