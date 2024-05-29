# Chase Sapphire Preferred

import re
import sys

sys.path.append('.')

from functions.inst_pars import extraction_func


# Dictionary keys to return.
stmt_essential_keys = ['month', 'balance', 'payment', 'points']
stmt_table_tx_dates = []
stmt_table_tx_merchants = []
stmt_table_tx_amount = []

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
def keyword_search(extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            # if there are 2 more lines of text, capture text
            if i + 2 < len(lines):
                return lines[i+2].strip()
    return None


''' Dictionary assignment functions '''


# Find statement's month.
def find_month(extracted_text):
    keyphrase = 'SCENARIO-1D'
    return_month = keyword_search(extracted_text,keyphrase)
    return month_rollback(return_month)


# Rollback find_month() return to correct month.
def month_rollback(stmt_month=str):
    var_month, var_year = stmt_month.split()
    for i, value in stmt_monthrollback.items():
        if value == var_month:
            var_month = stmt_monthrollback[i-1]
    return f"{var_month} {var_year}"


# Find statement's balance.
def find_new_balance(extracted_text):
    keyphrase = 'New Balance'
    return keyword_search(extracted_text,keyphrase)


# Find statement's minimum payment.
def find_min_payment(extracted_text):
    keyphrase = 'Minimum Payment Due:'
    return keyword_search(extracted_text,keyphrase)


# Find available reward points.
def find_available_points(extracted_text):
    keyphrase = 'redemption'
    return keyword_search(extracted_text,keyphrase)


# Find starting index for transaction dates.
def find_starting_dates(test):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    counter = None
    phrase = 'PURCHASE'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    for line_number, line in enumerate(extracted_text, start=1):
        if phrase in line:
            counter = line_number + 2 # add 2 to counter to start on dates
            if test:
                print(f"\nTEST: dates start at: {counter}")
            break
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
                        print(f"\nTEST: merchants start at {counter}")
                        print(f"TEST: first page's dates: {dates}")
                        print(f"TEST: {find_starting_dates}: completed.")
                    return dates, counter
    return dates, counter


# Collect first page's merchants.
def find_starting_merchants(test, merchant_counter):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    counter = None
    ending_phrase = '$ Amount'
    merchants = []
    while merchant_counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == merchant_counter:
                if ending_phrase != line.strip():
                    merchants.append(line.strip())
                    merchant_counter += 2
                else:
                    counter = line_number + 4
                    if test:
                        print(f"\nTEST: price starts at {counter}")
                        print(f"TEST: first page merchants: {merchants}")
                        print(f"TEST: {find_starting_merchants}: completed.")
                    return merchants, counter
    return merchants, counter


# Collect first page's amounts.
def find_starting_amounts(test, price_counter):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    counter = None
    price_amounts = []
    while price_counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == price_counter:
                try:
                    price_amounts.append(float(line))
                    price_counter += 2
                except ValueError:
                    counter = line_number - 2
                    if test:
                        print(f"\nTEST: price ends at {counter}")
                        print(f"TEST: first page amounts: {price_amounts}")
                        print(f"TEST: {find_starting_amounts}: completed.")
                    return price_amounts, counter
    return price_amounts, counter


# Collect second page's transaction dates.
def find_addl_dates1(test):
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
                        print(f"TEST: second page limit: {len(dates)}")
                        print(f"TEST: {find_addl_dates1}: completed.")
                    return dates, counter, len(dates)
    return dates, counter


# Collect second page's merchants.
def find_addl_merchants1(test, sp_mercounter):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'r') as file:
        extracted_text = file.readlines()
    counter = sp_mercounter
    ending_phrase = 'INTEREST CHARGED'
    merchants = []
    while counter < len(extracted_text):
        for line_number, line in enumerate(extracted_text, start=1):
            if line_number == counter:
                if ending_phrase != line.strip():
                    merchants.append(line.strip())
                    counter += 2
                else:
                    if test:
                        print(f"\nTEST: second pages merchants: {merchants}")
                        print(f"TEST: {find_addl_merchants1}: completed.")
                    return merchants
    return merchants


# Collect second page's amounts.
def find_addl_amounts1(test, limit):
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
                            print(f"TEST: {find_addl_amounts1}: completed.")
                        return price_amounts
    return price_amounts
    # return amounts


# Main function of script.
def main(test, extracted_text, stmt_essential_keys=stmt_essential_keys):
    if test:
        print(f"\n\nTEST: {main} running...")
    # Set up return statement.
    export_text = []
    stmt_essential_dict = {key: None for key in stmt_essential_keys}
    # Dictionary population functions.
    stmt_essential_dict['month'] = " ".join((find_month(extracted_text)).split()) # Removes double space.
    stmt_essential_dict['balance'] = (find_new_balance(extracted_text))
    stmt_essential_dict['payment'] = (find_min_payment(extracted_text))
    stmt_essential_dict['points'] = (find_available_points(extracted_text))
    # Pack export_text to return.
    export_text.append(stmt_essential_dict)
    fp_dates, fp_mercounter = find_starting_dates(test)
    fp_merchants, fp_pricounter = find_starting_merchants(test, fp_mercounter)
    fp_prices, fp_endcounter = find_starting_amounts(test, fp_pricounter) # NORMAL: fp_endcounter not referenced anywhere
    ''' need to collect next dates '''
    sp_dates, sp_mercounter, sp_limit = find_addl_dates1(test)
    ''' need to collect next merchants '''
    sp_merchants = find_addl_merchants1(test, sp_mercounter)
    ''' need to collect next prices '''
    sp_prices = find_addl_amounts1(test, sp_limit)
    # [Balance, Minimum Payment, Reward Points]
    if test:
        print(F"\nTEST: fnc return {export_text}")


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240111-statements-1149-.pdf'
    extracted_text = extraction_func(path)
    main(test, extracted_text)
    if test:
        print(f"TEST: {main} script completed.")