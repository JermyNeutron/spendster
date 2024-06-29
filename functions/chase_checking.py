# Chase Checking

import re
import sys

sys.path.append('.')

from functions.calendar_months import months_dict
from functions.create_csv import create_csv
from functions.inst_pars import extraction_func_def # Testing
from functions.unpack_dict import unpack_dict


# Transaction class (currently UNUSED).
class Transaction:
    def __init__(self, date, merchant, amount) -> None:
        self.date = date
        self.merchant = merchant
        self.amount = amount

    def __repr__(self) -> str:
        return f"Transaction({{{self.date}}}={self.date}, {{{self.merchant}}}={self.merchant}, {{{self.amount}}}={self.amount})"


# Centralized keyword scraping function.
def keyword_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> str:
    for i, line in enumerate(extracted_text):
        if keyphrase in line:
            if i + 1 < len(extracted_text):
                hints_enabled and print(f"HINT: Returning keyword_search: {extracted_text[i+1]}")
                return extracted_text[i+1]
    return None


# Find statement's month.
def find_month(hints_enabled: bool, extracted_text: list) -> tuple[str, str]:
    keyphrase = 'Columbus, OH 43218 - 2051'
    return_text = keyword_search(hints_enabled, extracted_text, keyphrase)
    return_text_split = return_text.split(' ')
    var_month, var_year = return_text_split[-3], return_text_split[-1]
    for i, month in months_dict.items():
        if var_month == month: # Redundant check of successful scrape.
            hints_enabled and print(f"HINT: Returning month {{{i}}}: {month} {var_year}")
            return f"{var_month} {var_year}", return_text
    return None


# Collect statement ending balance.
def find_ending_balance(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = "Ending Balance"
    occurences = []
    # Find line number for keyphrase.
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line:
            hints_enabled and print(f"HINT: {find_ending_balance}: {i}, {line.strip()}")
            occurences.append(i)
    # Find next line after keyphrase to return statement ending balance.
    counter = occurences.pop(0) + 1
    for i, line in enumerate(extracted_text, start=1):
        if counter == i:
            hints_enabled and print(f"HINT: Returning balance: {line}")
            return line.strip()


# Centralized scraping function.
def transaction_scrape(hints_enabled: bool, extracted_text: list, counter: int, end_phrase: str) -> list:
    date_format = re.compile(r'^\d{2}/\d{2}$')
    transactions_arr = []
    for i in range(1, len(extracted_text) + 1):
        if i == counter:
            j = counter - 1
            while j < len(extracted_text):
                if j + 3 < len(extracted_text):
                    if end_phrase not in extracted_text[j].strip():
                        # If [j] is a misc line to be skipped
                        if not date_format.match(extracted_text[j].strip()):
                            j += 1
                            continue
                        else:
                            trx_date = extracted_text[j].strip()
                            pre_trx_merchant = extracted_text[j + 1].strip()
                            trx_merchant = ' '.join(pre_trx_merchant.split())
                            trx_amount = extracted_text[j + 2].strip()
                            transaction_ind = (trx_date, trx_amount, trx_merchant)
                            transactions_arr.append(transaction_ind)
                            hints_enabled and print(f"HINT: {trx_date}, {trx_amount}, {trx_merchant}")
                            j += 4
                    else:
                        hints_enabled and print(f"HINT: Ending phrase met: {j - 1}: \"{extracted_text[j]}\"")
                        return transactions_arr
    return transactions_arr


# Collect first page transactions.
def find_starting_transactions(hints_enabled: bool, extracted_text: list) -> list:
    keyphrase = "Beginning Balance"
    end_phrase = "*end*transaction detail"
    occurences = []
    # Find line number for keyphrase.
    for i, line in enumerate(extracted_text, start=1):
        if keyphrase in line.strip():
            hints_enabled and print(f"HINT: {find_starting_transactions}: {i}, {line}")
            occurences.append(i)
    counter = occurences.pop() + 2
    if hints_enabled:
        print('\nHINT:', find_starting_transactions)
        print(f"HINT: Transactions start: {counter}")
    return transaction_scrape(hints_enabled, extracted_text, counter, end_phrase)


# Determine if second page transactions exist.
def is_adl(hints_enabled: bool, extracted_text: list):
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
    return sp_bool, None


# Scrape second page's transactions.
def find_adl_transactions(hints_enabled: bool, extracted_text: list, sp_counter: int) -> list:
    end_phrase = '*end*transaction detail'
    if hints_enabled:
        print('\nHINT:', find_adl_transactions)
        print(f"HINT: Second page counter starts: {sp_counter}")
    return transaction_scrape(hints_enabled, extracted_text, sp_counter, end_phrase)


# Main function of script.
def main(test: bool, hints_enabled: bool, extracted_text: list) -> None:
    stmt_essential_keys = ['month', 'period', 'balance',]
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    export_text = []
    if hints_enabled:
        print('\nHINT:', main)
        print(F"HINT: Statement CSV headers")
    stmt_essential_dict['month'], stmt_essential_dict['period'] = find_month(hints_enabled, extracted_text)
    stmt_essential_dict['balance'] = find_ending_balance(hints_enabled, extracted_text)
    export_text.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    transaction_arr: list[str] = find_starting_transactions(hints_enabled, extracted_text)
    export_text.extend(transaction_arr)
    adl_exit, sp_counter = is_adl(hints_enabled, extracted_text)
    if adl_exit:
        transaction_arr.extend(find_adl_transactions(hints_enabled, extracted_text, sp_counter))
        export_text.extend(transaction_arr)
    
    create_csv(test, hints_enabled, export_text)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    # path = 'rep_statements/20240320-statements-9266-.pdf'
    path = 'rep_statements/20240320-statements-9266-.pdf'
    with open(path, 'r', encoding="utf-8", errors="replace") as file:
        text = extraction_func_def(path)
    extracted_text = [item for item in text.split('\n') if item != '']
    main(test, hints_enabled, extracted_text)


'''
Commit Comments:
- 

'''