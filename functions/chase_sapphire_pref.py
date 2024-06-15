# Chase Sapphire Preferred

import csv
import re
import sys

sys.path.append('.')

import pyperclip

from functions.inst_pars import extraction_func


# Dictionary keys to return.
stmt_essential_keys = ['month', 'balance', 'payment', 'points']

# Month rollback for statement (February due date is January's statement)
stmt_monthrollback = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


# Scrape document.
def keyword_search(test, extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            # if there are 2 more lines of text, capture text
            if i + 2 < len(lines):
                if test:
                    print(f"TEST: returning {lines[i+2]}")
                return lines[i+2].strip()
    return None


''' Dictionary assignment functions '''


# Find statement's month.
def find_month(test, extracted_text):
    keyphrase = 'SCENARIO-1D'
    return_month = keyword_search(test, extracted_text, keyphrase)
    return month_rollback(return_month)


# Rollback find_month() return to correct month.
def month_rollback(stmt_month=str):
    var_month, var_year = stmt_month.split()
    for i, value in stmt_monthrollback.items():
        if value == var_month:
            var_month = stmt_monthrollback[i-1]
    return f"{var_month} {var_year}"


# Find statement's balance.
def find_new_balance(test, extracted_text):
    keyphrase = 'New Balance'
    return keyword_search(test, extracted_text, keyphrase)


# Find statement's minimum payment.
def find_min_payment(test, extracted_text):
    keyphrase = 'Minimum Payment Due:'
    return keyword_search(test, extracted_text, keyphrase)


# Find available reward points.
def find_available_points(test, extracted_text):
    keyphrase = 'redemption'
    return keyword_search(test, extracted_text, keyphrase)


# Unpack stmt_essential_dict items into csv
def unpack_dict(stmt_essential_dic: dict):
    keyval_pair = []
    for key, value in stmt_essential_dic.items():
        keyval_pair.append((key, value))
    return keyval_pair


''' First page scraping '''

# Find starting index for transaction dates.
def find_starting_dates(test):


    # Count preceding dates to determine text gap to merchants
    def count_backward(test, retro_counter):
        line_skip = 0
        skip_array = []
        retro_counter -= 2
        while retro_counter < len(extracted_text):
            for line_number, line in enumerate(extracted_text, start=1):
                if line_number == retro_counter:
                    if date_pattern.match(line.strip()):
                        line_skip += 2
                        skip_array.append(line.strip())
                        retro_counter -= 2
                    else:
                        if test:
                            print(f"TEST: skipping {{{int(line_skip/2)}}} lines:")
                            print(*(i for i in skip_array), sep='\n')
                        return line_skip


    def count_forward(test, counter):
        while counter < len(extracted_text):
            for line_number, line in enumerate(extracted_text, start=1):
                if line_number == counter:
                    if date_pattern.match(line.strip()):
                        dates.append(line.strip())
                        counter += 2
                    else:
                        if test:
                            print(find_starting_dates)
                            print(f"TEST: merchants start at {counter}")
                            print(f"TEST: first page's dates: {dates}")
                            print(f"TEST: array lenth: {len(dates)}")
                            print(f"TEST: {find_starting_dates}: completed.")
                        return dates, counter
                    

    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    retro_counter = 0
    counter = 0
    phrase = 'PURCHASE'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase in line:
            retro_counter = line_number # counter for count_backwards()
            counter = line_number + 2 # add 2 to counter to start on dates
            if test:
                print(f"\nTEST: dates start at: {counter}")
            break
    dates = []
    date_pattern = re.compile(r'^\d{2}/\d{2}$')
    line_skip = count_backward(test, retro_counter)
    dates, counter = count_forward(test, counter)
    return dates, counter, line_skip


# Collect first page's merchants.
def find_starting_merchants(test, merchant_counter, line_skip):


    # Redudant counter for '$ Amount'
    def find_price_counter():
        counter: int = 0
        ending_phrase_1 = "$ Amount"
        for line_number, line in enumerate(extracted_text, start=1):
            if line.strip() == ending_phrase_1:
                counter = line_number
                return counter


    if line_skip is None:
        line_skip = 0
    if test:
        print(find_starting_merchants)
        print(f"TEST: starting variable {{test}}: {test}")
        print(f"TEST: starting variable {{merchant_counter}}: {merchant_counter}")
        print(f"TEST: starting variable {{line_skip}}: {line_skip}")
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
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
                        merchant_counter += 2
                    else:
                        ending_flag = line.strip()
                        counter = find_price_counter()
                        if test:
                            print(f"TEST: first page merchants: {merchants}")
                            print(f"TEST: array length: {len(merchants)}")
                            print(f"TEST: ending phrase caught: \"{ending_flag}\"")
                            print(f"TEST: price starts at {counter}")
                            print(f"TEST: {find_starting_merchants}: completed.")
                        return merchants, counter, reject_counter
                else:
                    merchant_counter += 2
                    reject_counter += 1
    return merchants, counter, reject_counter


# Collect first page's amounts.
def find_starting_amounts(test, price_counter, line_skip, reject_counter):
    if line_skip is None:
        line_skip = 0
    if test:
        print(f"\nTEST: starting variable {{test}}: {test}")
        print(f"TEST: starting variable {{price_counter}}: {price_counter}")
        print(f"TEST: starting variable {{line_skip}}: {line_skip}")
        print(f"TEST: starting variable {{reject_counter}}: {reject_counter}")
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    counter = None
    price_amounts = []
    differential = 0
    if line_skip == 0:
        differential = 2
    price_counter = price_counter + 2 + line_skip + differential
    while price_counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == price_counter:
                try:
                    price_amounts.append(float(line))
                    price_counter += 2
                except ValueError:
                    counter = line_number - 2
                    if reject_counter != 0:
                        del price_amounts[-reject_counter:]
                    if test:
                        print(f"TEST: reject_counter end: {reject_counter}")
                        print(f"TEST: first page amounts: {price_amounts}")
                        print(f"TEST: array length: {len(price_amounts)}")
                        print(f"TEST: price ends at {counter}")
                        print(f"TEST: {find_starting_amounts}: completed.")
                    return price_amounts, counter
    return price_amounts, counter


''' Second page scraping '''


# Determine if there is a second transaction page.
def is_sp(test):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    phrase = "Date of\n"
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase == line:
            occurrences.append(line_number)
    if len(occurrences) >= 2:
        if test:
           print('\nTEST: There are multiple pages of transactions')
           print(f"TEST: Occurrences: {occurrences}")
        return True
    else:
        if test:
           print('\nTEST: There is only one page of transactions')
           print(f"TEST: Occurrences: {occurrences}")
        return False


# Collect second page's transaction dates.
def find_addl_dates(test):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    phrase = 'Date of\n'
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if line == phrase:
            occurrences.append((line_number))
    counter = occurrences.pop() + 3
    dates = []
    date_pattern = re.compile(r'^\d{2}/\d{2}$')
    while counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == counter:
                if date_pattern.match(line.strip()):
                    dates.append(line.strip())
                    counter += 2
                else:
                    if test:
                        counter += 2
                        print(f"\nTEST: second page's merchants start at {counter}")
                        print(f"TEST: second page's dates: {dates}")
                        print(f"TEST: array length: {len(dates)}")
                        print(f"TEST: {find_addl_dates}: completed.")
                    return dates, counter, len(dates)
    return dates, counter


# Collect second page's merchants.
def find_addl_merchants(test, sp_mercounter):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    counter = sp_mercounter
    ending_phrases = ['INTEREST CHARGED\n', 'FEES CHARGED\n']
    merchants = []
    while counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == counter:
                if any(line == phrase for phrase in ending_phrases):
                    if test:
                        print(f"\nTEST: second pages merchants: {merchants}")
                        print(f"TEST: array length: {len(merchants)}")
                        print(f"TEST: {find_addl_merchants}: completed.")
                    return merchants
                merchants.append(line.strip())
                counter += 2
    return merchants


# Collect second page's amounts.
def find_addl_amounts(test, limit):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    phrase = "$ Amount\n"
    occurrences = []
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase == line:
            occurrences.append(line_number)
    placement = occurrences.pop() + 2
    price_amounts = []
    while placement < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == placement:
                if len(price_amounts) < limit:
                    price_amounts.append(float(line))
                    placement += 2
                    if len(price_amounts) == 2:
                        if test:
                            print(f"\nTEST: second page amounts: {price_amounts}")
                            print(f"TEST: array length: {len(price_amounts)}")
                            print(f"TEST: {find_addl_amounts}: completed.")
                        return price_amounts
    return price_amounts
    # return amounts


# Pack and write organized data into csv.
def create_csv(test, export_text):
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
def main(test, extracted_text, stmt_essential_keys=stmt_essential_keys):
    if test:
        print(f"\n\nTEST: {main} running...\n")
    # Set up return statement.
    export_text = []
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    # Dictionary population functions.
    stmt_essential_dict['month'] = " ".join((find_month(test, extracted_text)).split()) # Removes double space.
    stmt_essential_dict['balance'] = (find_new_balance(test, extracted_text))
    stmt_essential_dict['payment'] = (find_min_payment(test, extracted_text))
    stmt_essential_dict['points'] = (find_available_points(test, extracted_text))
    # Pack export_text to return.
    export_text.extend(unpack_dict(stmt_essential_dict))
    stmt_transactions = [('Dates', 'Merchants', 'Amount')]
    fp_dates, fp_mercounter, fp_skipnum = find_starting_dates(test)
    fp_merchants, fp_pricounter, fp_rejectcounter = find_starting_merchants(test, fp_mercounter, fp_skipnum)
    fp_prices, fp_endcounter = find_starting_amounts(test, fp_pricounter, fp_skipnum, fp_rejectcounter) # NORMAL: fp_endcounter not referenced anywhere
    stmt_transactions.extend(zip(fp_dates, fp_prices, fp_merchants))
    if is_sp(test):
        sp_dates, sp_mercounter, sp_limit = find_addl_dates(test)
        sp_merchants = find_addl_merchants(test, sp_mercounter)
        sp_prices = find_addl_amounts(test, sp_limit)
        stmt_transactions.extend(zip(sp_dates, sp_prices, sp_merchants))
        print('TEST: second page completed.')
    export_text.extend(stmt_transactions)
    # [Balance, Minimum Payment, Reward Points]
    if test:
        print(F"\nTEST: fnc return {stmt_essential_dict}")
    create_csv(test, export_text)


if __name__ == '__main__':
    test = True
    option_1 = 'rep_statements/20240111-statements-1149-.pdf'
    option_2 = 'rep_statements/20240511-statements-1149-.pdf'
    choice = input('Choose path: ')
    if choice == '1':
        path = option_1
    elif choice == '2':
        path = option_2
    else:
        path = option_1
    extracted_text = extraction_func(path)
    main(test, extracted_text)
    if test:
        print(f"TEST: {main} script completed.")


'''
Commit Comments:
- 

'''