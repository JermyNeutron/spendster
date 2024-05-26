# Chase Sapphire Preferred

import sys
sys.path.append('.')

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
def keyword_search(extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            # if there are 2 more lines of text, capture text
            if i + 2 < len(lines):
                return lines[i+2].strip()
    return None


''' Dictionary assignment functions '''

# Rollback to correct month.
def month_rollback(stmt_month=str):
    var_month, var_year = stmt_month.split()
    for i, value in stmt_monthrollback.items():
        if value == var_month:
            var_month = stmt_monthrollback[i-1]
    return f"{var_month} {var_year}"


# Find statement's month.
def find_month(extracted_text):
    keyphrase = 'SCENARIO-1D'
    return_month = keyword_search(extracted_text,keyphrase)
    return month_rollback(return_month)


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


# Main function of script.
def main(test, extracted_text, stmt_essential_keys=stmt_essential_keys):
    if test:
        print("TEST:", main)
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
    # [Balance, Minimum Payment, Reward Points]
    if test:
        print(export_text)


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240111-statements-1149-.pdf'
    extracted_text = extraction_func(path)
    main(test, extracted_text)