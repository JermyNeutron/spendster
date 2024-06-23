# Schoolsfirst Checking
import re
import warnings

import pyperclip

from .calendar_months import months_dict # preceding '.' for main.py execution


# Dictionary keys to return.
stmt_essential_keys = ['month', 'starting balance', 'ending balance']


# Text cleaning.
def fil_text(uf_text: str) -> list:
    rm_wspce = re.sub(r'\s{3,}', ',', uf_text.strip())
    uf_extracted = rm_wspce.split(',')
    extracted_text = []
    for item in uf_extracted:
        if '\n' in item:
            parts = item.split('\n')
            extracted_text.extend(parts)
        else:
            extracted_text.append(item)
    return extracted_text


# Collect statement month.
def find_month(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = "Date:"
    for item in extracted_text:
        if keyphrase in item:
            if hints_enabled:
                print('\nHINT:', find_month)
                print(f"HINT: Statement Date: {item.strip(keyphrase)}")
            return item.strip(keyphrase)


# Collect statement starting balace.
def find_starting_bal(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'CHECKING Balance Forward'
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            if hints_enabled:
                print('\nHINT:', find_starting_bal)
                print(f'HINT: Starting balance: {extracted_text[i]}')
            return extracted_text[i]
        

# Collect statement ending balance.
def find_ending_bal(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'Ending Balance'
    occurences:int = []
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            occurences.append(i)
    ending_bal = occurences[-1]
    if hints_enabled:
        print('\nHINT:', find_ending_bal)
        print('HINT:', occurences)
        print(f'HINT: Ending balance: {extracted_text[ending_bal]}')
    return extracted_text[ending_bal]


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


# Main function of script.
def main(test: bool, hints_enabled: bool, uf_text: str):
    warnings.warn('main() not developed yet')
    hints_enabled and print('sfcu_checking.main() executing...')
    export_text = []
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    extracted_text = fil_text(uf_text)
    stmt_essential_dict['month'] = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['starting balance'] = find_starting_bal(hints_enabled, extracted_text)
    stmt_essential_dict['ending balance'] = find_ending_bal(hints_enabled, extracted_text)
    export_text.extend(unpack_dict(hints_enabled, stmt_essential_dict))


if __name__ == '__main__':
    # Simulated inputs
    test = True
    hints_enabled = True
    # Make sure test path is correctly populated
    path = 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        uf_text = file.read()
    # End simulated inputs

    main(test, hints_enabled, uf_text)


'''
Commit Comments:
- 

'''