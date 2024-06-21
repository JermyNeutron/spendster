# Institution Parser
from pdfminer.high_level import extract_text as pdfmextract_text


'''Supported Institutions and Statements
- Chase Sapphire Preferred
- Chase Debit (WIP)
'''

list_institutions = {
    'Chase': ['Sapphire Preferred', 'Chase debit',]
}


# Extract text from the provided path.
def extraction_func(path):
    text = pdfmextract_text(path)
    return text


# Write the extracted text to temp file.
def extraction_writing(test, text):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    extracted_text = [item.strip() for item in text.split('\n') if item != '']
    with open(path, 'w', encoding="utf-8", errors="replace") as file:
        for i in extracted_text:
            file.write(f"{i}\n")


# Parse text to identify the institution.
def ident_inst(hints_enabled, extracted_text):
    for inst, keywords in list_institutions.items():
        for keyword in keywords:
            if keyword in extracted_text:
                if hints_enabled:
                    print(f"HINT: {{inst}}: {inst}")
                    print(f"HINT: {{keyword}}: {keyword}")
                return inst, keyword


# Main function of script.
def main(test, hints_enabled, path):
    extracted_text = extraction_func(path)
    inst_select, inst_doc = ident_inst(hints_enabled, extracted_text)
    if inst_select == 'Chase':
        if hints_enabled:
            print(f'HINT: {ident_inst}: INSTITUTION FOUND: Chase {inst_doc}')
            print(f'HINT: returning {inst_select}, {inst_doc}')
    else: # change to elif
        if hints_enabled:
            pass
        return None
    extraction_writing(test, extracted_text)
    return inst_select, inst_doc


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path_1 = 'rep_statements/20240111-statements-1149-.pdf'
    path_2 = 'rep_statements/20240511-statements-1149-.pdf'
    path_3 = 'rep_statements/20240320-statements-9266-.pdf'
    test_choice = input('Choose path: ')
    try:
        if test_choice == '1':
            institution, document = main(test, hints_enabled, path_1)
        elif test_choice == '2':
            institution, document = main(test, hints_enabled, path_2)
        elif test_choice == '3':
            institution, document = main(test, hints_enabled, path_3)
    except NameError as e:
        print('Invalid choice.')
        