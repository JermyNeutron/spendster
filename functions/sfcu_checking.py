# Schoolsfirst Checking

import re
import warnings

from functions.inst_pars import extraction_writing
from functions.create_csv import create_csv
from functions.unpack_dict import unpack_dict


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
def find_starting_bal(hints_enabled: bool, extracted_text: list) -> tuple[str, int]:
    keyphrase = 'CHECKING Balance Forward'
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            if hints_enabled:
                print('\nHINT:', find_starting_bal)
                print(f'HINT: Starting balance: {extracted_text[i]}')
                print(f'HINT: counter starts at {i}')
            return extracted_text[i], i
        

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


def fil_trx(hints_enabled: bool, extracted_text: list,) -> list:
    filtered_text = []
    flags = []
    trx_pattern = re.compile(r'^\d{2}.\d{2}-')
    for item in extracted_text:
        if trx_pattern.match(item):
            str_split = item.split()
            str_split = [s.rstrip('-') for s in str_split]
            filtered_text.extend(str_split)
            flags.append(item)
        else:
            filtered_text.append(item)
    hints_enabled and print('HINT:', fil_trx, 'HINT: ', flags, '\n...')
    return filtered_text


def find_transactions(hints_enabled: bool, extracted_text: list, counter: int) -> list:


    # Removes any amounts in merchant string
    def rm_amt(merchant: str) -> str:
        temp_var = merchant.split()
        if '.' in temp_var[-1]:
            temp_var.pop()
        return_var = ' '.join(i for i in temp_var)
        return return_var


    transactions_arr: list = []
    date_format = re.compile(r'^\d{2}/\d{2}$')
    ending_phrase = 'Combined Minimum Balance'
    hints_enabled and print('HINT:', find_transactions)
    extracted_text = fil_trx(hints_enabled, extracted_text)
    for i in range(1, len(extracted_text) + 1):
        if i == counter:
            j = counter + 1
            while j < len(extracted_text):
                if j + 2 < len(extracted_text):
                    if ending_phrase in extracted_text[j+1]:
                        hints_enabled and print(f'HINT: returning transaction array: {transactions_arr}')
                        return transactions_arr
                    if not date_format.match(extracted_text[j].strip()):
                        j+=1
                        continue
                    else:
                        trx_date = extracted_text[j].strip()

                        # Removes any attached amounts to merchant string.
                        temp_merchant = ' '.join([extracted_text[j+1], extracted_text[j+4]])
                        trx_merchant = rm_amt(temp_merchant)

                        # If no skip phrases, checks to see if [j+2] is an amount.
                        try:
                            temp_str = extracted_text[j+2].strip().split()[0].rstrip('-')
                            float(temp_str)
                            trx_amount = temp_str
                        except ValueError as e:
                            temp_str = extracted_text[j+3].strip().split()[0].rstrip('-')
                            float(temp_str)
                            hints_enabled and print(f'valueerror: {temp_str}')
                            trx_amount = temp_str

                        trx_ind = (trx_date, trx_amount, trx_merchant)
                        transactions_arr.append(trx_ind)
                        hints_enabled and print(f"HINT: {trx_date}, {trx_amount}, {trx_merchant}")
                        j+=5


# Main function of script.
def main(test: bool, hints_enabled: bool, uf_text: str) -> None:
    hints_enabled and print('sfcu_checking.main() executing...')
    export_text = []
    stmt_essential_keys = ['month', 'starting balance', 'ending balance']
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    extracted_text = fil_text(uf_text)
    stmt_essential_dict['month'] = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['starting balance'], counter = find_starting_bal(hints_enabled, extracted_text)
    stmt_essential_dict['ending balance'] = find_ending_bal(hints_enabled, extracted_text)
    export_text.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    transaction_arr = find_transactions(hints_enabled, extracted_text, counter)
    export_text.extend(transaction_arr)
    create_csv(test, hints_enabled, export_text)


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