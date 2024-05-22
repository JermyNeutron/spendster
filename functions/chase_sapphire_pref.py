# Chase Sapphire Preferred

import sys
sys.path.append('.')

from functions.inst_pars import extraction_func



# scrape document
def keyword_search(extracted_text, keyphrase):
    lines = extracted_text.splitlines()
    for i, line in enumerate(lines):
        if keyphrase in line:
            # if there are 2 more lines of text, capture text
            if i + 2 < len(lines):
                return lines[i+2].strip()
    return None


# Find statement's balance
def find_new_balance(extracted_text):
    keyphrase = 'New Balance'
    return keyword_search(extracted_text,keyphrase)


# Find statement's minimum payment
def find_min_payment(extracted_text):
    keyphrase = 'Minimum Payment Due:'
    return keyword_search(extracted_text,keyphrase)


# Find available reward points
def find_available_points(extracted_text):
    keyphrase = 'redemption'
    return keyword_search(extracted_text,keyphrase)


def main(test, extracted_text):
    if test:
        print("TEST:", main)
    export_text = []
    export_text.append(find_new_balance(extracted_text))
    export_text.append(find_min_payment(extracted_text))
    export_text.append(find_available_points(extracted_text))
    print(export_text)


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240111-statements-1149-.pdf'
    extracted_text = extraction_func(path)
    main(test, extracted_text)