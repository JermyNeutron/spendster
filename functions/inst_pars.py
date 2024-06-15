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
    with open(path, 'w') as file:
        file.write(text)


# Parse text to identify the institution.
def ident_inst(test, extracted_text):
    for inst, keywords in list_institutions.items():
        for keyword in keywords:
            if keyword in extracted_text:
                if test:
                    print(f"TESt: {{inst}}: {inst}")
                    print(f"TEST: {{keyword}}: {keyword}")
                return inst, keyword


# Main function of script.
def main(test, path):
    extracted_text = extraction_func(path)
    inst_select, inst_doc = ident_inst(test, extracted_text)
    if test:
        if inst_select == 'Chase':
            print(f'TEST: {ident_inst}: INSTITUTION FOUND: Chase {inst_doc}')
        else: # change to elif
            return None
    extraction_writing(test, extracted_text)
    return inst_select, inst_doc


if __name__ == '__main__':
    test = True
    path_1 = 'rep_statements/20240111-statements-1149-.pdf'
    path_2 = 'rep_statements/20240511-statements-1149-.pdf'
    path_3 = 'rep_statements/20240320-statements-9266-.pdf'
    test_choice = input('Choose path: ')
    try:
        if test_choice == '1':
            institution, document = main(test, path_1)
        elif test_choice == '2':
            institution, document = main(test, path_2)
        elif test_choice == '3':
            institution, document = main(test, path_3)
    except NameError as e:
        print('Invalid choice.')
        