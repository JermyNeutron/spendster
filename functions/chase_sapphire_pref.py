# Chase Sapphire Preferred

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func_def
from .calendar_months import months_dict # preceding '.' for main.py execution


# Dictionary keys to return.
stmt_essential_keys = ['month', 'balance', 'payment', 'points']


# Scrape document.
def keyword_search(hints_enabled: bool, extracted_text: list, keyphrase: str) -> str:
    # lines = extracted_text.splitlines()
    for i, line in enumerate(extracted_text):
        if keyphrase in line:
            # if there are 2 more lines of text, capture text
            if i + 2 < len(extracted_text):
                hints_enabled and print(f"HINT: returning {extracted_text[i+1]}")
                return extracted_text[i+1].strip()
    return None


''' Dictionary assignment functions '''


# Find statement's month.
def find_month(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'SCENARIO-1D'
    return_month = keyword_search(hints_enabled, extracted_text, keyphrase)
    return month_rollback(return_month)


# Rollback find_month() return to correct month.
def month_rollback(stmt_month: str) -> str:
    var_month, var_year = stmt_month.split()
    for i, value in months_dict.items():
        if value == var_month:
            var_month = months_dict[i-1]
    return f"{var_month} {var_year}"


# Find statement's balance.
def find_new_balance(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'New Balance'
    return keyword_search(hints_enabled, extracted_text, keyphrase)


# Find statement's minimum payment.
def find_min_payment(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'Minimum Payment Due:'
    return keyword_search(hints_enabled, extracted_text, keyphrase)


# Find available reward points.
def find_available_points(hints_enabled: bool, extracted_text: list) -> str:
    keyphrase = 'redemption'
    return keyword_search(hints_enabled, extracted_text, keyphrase)


# Unpack stmt_essential_dict items into csv
def unpack_dict(hints_enabled: bool, stmt_essential_dict: dict) -> list:
    keyval_pair = []
    for key, value in stmt_essential_dict.items():
        keyval_pair.append((key, value))
    hints_enabled and print('\nHINT: Unpacking dictionary...')
    return keyval_pair


''' First page scraping '''

# Find starting index for transaction dates.
def find_starting_dates(hints_enabled: bool, extracted_text: list) -> tuple[list, int, int]:


    # Count preceding dates to determine text gap to merchants
    def count_backward(hints_enabled: bool, retro_counter: int) -> int:
        line_skip = 0
        skip_array = []
        retro_counter -= 1
        while retro_counter < len(extracted_text):
            for line_number, line in enumerate(extracted_text, start=1):
                if line_number == retro_counter:
                    if date_pattern.match(line.strip()):
                        line_skip += 1
                        skip_array.append(line.strip())
                        retro_counter -= 1
                    else:
                        if hints_enabled:
                            print(f"HINT: skipping {{{int(line_skip/2)}}} lines:")
                            print(*(i for i in skip_array), sep='\n')
                        return line_skip


    def count_forward(hints_enabled: bool, counter: int) -> tuple[list, int]:
        while counter < len(extracted_text):
            for line_number, line in enumerate(extracted_text, start=1):
                if line_number == counter:
                    if date_pattern.match(line.strip()):
                        dates.append(line.strip())
                        counter += 1
                    else:
                        if hints_enabled:
                            print(find_starting_dates)
                            print(f"HINT: merchants start at {counter}")
                            print(f"HINT: first page's dates: {dates}")
                            print(f"HINT: array lenth: {len(dates)}")
                            print(f"HINT: {find_starting_dates}: completed.")
                        return dates, counter
                    

    retro_counter = 0
    counter = 0
    phrase = 'PURCHASE'
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase in line:
            retro_counter = line_number # counter for count_backwards()
            counter = line_number + 1 # add 1 to counter to start on dates
            hints_enabled and print(f"\nHINT: dates start at: {counter}")
            break
    dates = []
    date_pattern = re.compile(r'^\d{2}/\d{2}$')
    line_skip = count_backward(hints_enabled, retro_counter)
    dates, counter = count_forward(hints_enabled, counter)
    return dates, counter, line_skip


# Collect first page's merchants.
def find_starting_merchants(hints_enabled:bool, extracted_text: list, merchant_counter: int, line_skip: int) -> tuple[list, int, int]:


    # Redudant counter for '$ Amount'
    def find_price_counter() -> int:
        counter: int = 0
        ending_phrase_1 = "$ Amount"
        for line_number, line in enumerate(extracted_text, start=1):
            if line.strip() == ending_phrase_1:
                counter = line_number
                return counter


    if line_skip is None:
        line_skip = 0
    if hints_enabled:
        print('\nHINT: ', find_starting_merchants)
        print(f"HINT: starting variable {{merchant_counter}}: {merchant_counter}")
        print(f"HINT: starting variable {{line_skip}}: {line_skip}")
    counter = None
    reject_patterns = [r'^\d{6}',]
    reject_counter = 0
    ending_phrases = ['INTEREST CHARGED', 'FEES CHARGED', '$ Amount']
    ending_flag = ""
    merchants = []
    merchant_counter += line_skip
    while merchant_counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == merchant_counter:
                if not any(re.match(pattern, line.strip()) for pattern in reject_patterns):
                    if not any(line.strip() == phrase for phrase in ending_phrases):
                        merchants.append(line.strip())
                        merchant_counter += 1
                    else:
                        ending_flag = line.strip()
                        counter = find_price_counter()
                        if hints_enabled:
                            print(f"HINT: first page merchants: {merchants}")
                            print(f"HINT: array length: {len(merchants)}")
                            print(f"HINT: ending phrase caught: \"{ending_flag}\"")
                            print(f"HINT: price starts at {counter}")
                            print(f"HINT: {find_starting_merchants}: completed.")
                        return merchants, counter, reject_counter
                else:
                    merchant_counter += 1
                    reject_counter += 1
    return merchants, counter, reject_counter


# Collect first page's amounts.
def find_starting_amounts(hints_enabled: bool, extracted_text: list, price_counter: int, line_skip: int, reject_counter: int) -> tuple[list, int]:
    if line_skip is None:
        line_skip = 0
    if hints_enabled:
        print(f"\nHINT: starting variable {{price_counter}}: {price_counter}")
        print(f"HINT: starting variable {{line_skip}}: {line_skip}")
        print(f"HINT: starting variable {{reject_counter}}: {reject_counter}")
    counter = None
    price_amounts = []
    differential = 0
    if line_skip == 0:
        differential = 1
    price_counter = price_counter + 1 + line_skip + differential
    while price_counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == price_counter:
                try:
                    price_amounts.append(float(line))
                    price_counter+=1
                except ValueError:
                    counter = line_number - 2
                    if reject_counter != 0:
                        del price_amounts[-reject_counter:]
                    if hints_enabled:
                        print(f"HINT: reject_counter end: {reject_counter}")
                        print(f"HINT: first page amounts: {price_amounts}")
                        print(f"HINT: array length: {len(price_amounts)}")
                        print(f"HINT: price ends at {counter}")
                        print(f"HINT: {find_starting_amounts}: completed.")
                    return price_amounts, counter
    return price_amounts, counter


''' Second page scraping '''


# Determine if there is a second transaction page.
def is_sp(hints_enabled:bool, extracted_text: list) -> bool:
    phrase = "Date of"
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase == line:
            occurrences.append(line_number)
    if len(occurrences) >= 2:
        if hints_enabled:
           print('\nHINT: There are multiple pages of transactions')
           print(f"HINT: Occurrences: {occurrences}")
        return True
    else:
        if hints_enabled:
           print('\nHINT: There is only one page of transactions')
           print(f"HINT: Occurrences: {occurrences}")
        return False


# Collect second page's transaction dates.
def find_addl_dates(hints_enabled: bool, extracted_text: list) -> tuple[list, int]:
    phrase = 'Date of'
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if line == phrase:
            occurrences.append((line_number))
    counter = occurrences.pop() + 2
    dates = []
    date_pattern = re.compile(r'^\d{2}/\d{2}$')
    while counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == counter:
                if date_pattern.match(line.strip()):
                    dates.append(line.strip())
                    counter += 1
                else:
                    if hints_enabled:
                        counter += 1
                        print(f"\nHINT: second page's merchants start at {counter}")
                        print(f"HINT: second page's dates: {dates}")
                        print(f"HINT: array length: {len(dates)}")
                        print(f"HINT: {find_addl_dates}: completed.")
                    return dates, counter, len(dates)
    return dates, counter


# Collect second page's merchants.
def find_addl_merchants(hints_enabled: bool, extracted_text: list, sp_mercounter: int) -> list:
    counter = sp_mercounter
    ending_phrases = ['INTEREST CHARGED', 'FEES CHARGED']
    merchants = []
    while counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == counter:
                if any(line == phrase for phrase in ending_phrases):
                    if hints_enabled:
                        print(f"\nHINT: second pages merchants: {merchants}")
                        print(f"HINT: array length: {len(merchants)}")
                        print(f"HINT: {find_addl_merchants}: completed.")
                    return merchants
                merchants.append(line.strip())
                counter += 1
    return merchants


# Collect second page's amounts.
def find_addl_amounts(hints_enabled: bool, extracted_text: list, limit: int) -> list:
    phrase = "$ Amount"
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase == line:
            occurrences.append(line_number)
    placement = occurrences.pop() + 1
    price_amounts = []
    while placement < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == placement:
                if len(price_amounts) < limit:
                    price_amounts.append(float(line))
                    placement += 1
                    if len(price_amounts) == 2:
                        if hints_enabled:
                            print(f"\nHINT: second page amounts: {price_amounts}")
                            print(f"HINT: array length: {len(price_amounts)}")
                            print(f"HINT: {find_addl_amounts}: completed.")
                        return price_amounts
    return price_amounts


# Pack and write organized data into csv.
def create_csv(test: bool, export_text: list) -> None:
    path = 'temp/temp.csv' if not test else 'temp/test_temp.csv'
    with open(path, mode='w', newline='') as file: # writes CSV
        writer = csv.writer(file)
        writer.writerows(export_text)
    with open(path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        formatted_data = '\n'.join('\t'.join(row) for row in csv_data)
        pyperclip.copy(formatted_data)
        print("CSV content has been copied to clipboard. You can now paste it using CTRL+V.")
    if test: # converts type: list into string to write into .txt
        csv_view = 'temp/test_csv_view.txt'
        with open(csv_view, 'w') as file:
            for item in export_text:
                file.write(f"{str(item)}\n")
        print('TEST: csv view created...')


# Main function of script.
def main(test: bool, hints_enabled: bool, extracted_text: list, stmt_essential_keys: list = stmt_essential_keys) -> None:
    hints_enabled and print(f"\n\nHINT: {main} running...\n")
    # Set up return statement.
    export_text = []
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    # Dictionary population functions.
    stmt_essential_dict['month'] = " ".join((find_month(hints_enabled, extracted_text)).split()) # Removes double space.
    stmt_essential_dict['balance'] = (find_new_balance(hints_enabled, extracted_text))
    stmt_essential_dict['payment'] = (find_min_payment(hints_enabled, extracted_text))
    stmt_essential_dict['points'] = (find_available_points(hints_enabled, extracted_text))
    # Pack export_text to return.
    export_text.extend(unpack_dict(hints_enabled, stmt_essential_dict))
    stmt_transactions = [('Dates', 'Merchants', 'Amount')]
    fp_dates, fp_mercounter, fp_skipnum = find_starting_dates(hints_enabled, extracted_text)
    fp_merchants, fp_pricounter, fp_rejectcounter = find_starting_merchants(hints_enabled, extracted_text, fp_mercounter, fp_skipnum)
    fp_prices, fp_endcounter = find_starting_amounts(hints_enabled, extracted_text, fp_pricounter, fp_skipnum, fp_rejectcounter) # NORMAL: fp_endcounter not referenced anywhere
    stmt_transactions.extend(zip(fp_dates, fp_prices, fp_merchants))
    if is_sp(hints_enabled, extracted_text):
        sp_dates, sp_mercounter, sp_limit = find_addl_dates(hints_enabled, extracted_text)
        sp_merchants = find_addl_merchants(hints_enabled, extracted_text, sp_mercounter)
        sp_prices = find_addl_amounts(hints_enabled, extracted_text, sp_limit)
        stmt_transactions.extend(zip(sp_dates, sp_prices, sp_merchants))
        hints_enabled and print('HINT: second page completed.')
    export_text.extend(stmt_transactions)
    # [Balance, Minimum Payment, Reward Points]
    hints_enabled and print(F"\nHINT: fnc return {stmt_essential_dict}")
    create_csv(test, export_text)


if __name__ == '__main__':
    test = True
    hints_enabled = True
    option_1 = 'rep_statements/20240111-statements-1149-.pdf'
    option_2 = 'rep_statements/20240511-statements-1149-.pdf'
    choice = input('Choose path: ')
    if choice == '1':
        path = option_1
    elif choice == '2':
        path = option_2
    else:
        path = option_1
    text = extraction_func_def(path)
    extracted_text = [item for item in text.split('\n') if item != '']
    main(test, hints_enabled, extracted_text)
    if test:
        print(f"TEST: {main} script completed.")


'''
Commit Comments:
- 

'''