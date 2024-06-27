# Institution Parser
import warnings

from pdfminer.high_level import extract_text as pdfmextract_text


'''Supported Institutions and Statements
- Chase Sapphire Preferred
- Chase Checking
- PayPal Credit
- SchoolsFirst Checking
- SchoolsFirst Inspire
- Synchrony Car Care
'''

list_institutions = {
    'Chase': ['Sapphire Preferred', 'Chase debit',],
    'SchoolsFirst': ['www.SchoolsFirstFcu.org', 'www.SchoolsFirstfcu.org',], # save 'MasterCard' if URL ever gets fixed on Checking
    'Synchrony': ['SYNCHRONY CAR CARE',],
    'PayPal': ['PayPal Credit',],
}


# Extract text from the provided path.
def extraction_func(path: str) -> str:
    text = pdfmextract_text(path)
    return text


# Write the extracted text to temp file.
def extraction_writing(test: bool, text: str) -> None:
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    extracted_text = [item.strip() for item in text.split('\n') if item != '']
    with open(path, 'w', encoding="utf-8", errors="replace") as file:
        for i in extracted_text:
            file.write(f"{i}\n")


# Parse text to identify the institution.
def ident_inst(hints_enabled: bool, extracted_text: list) -> tuple[str, str]:
    for inst, keywords in list_institutions.items():
        for keyword in keywords:
            if keyword in extracted_text:
                if hints_enabled:
                    print(f"HINT: {{inst}}: {inst}")
                    print(f"HINT: {{keyword}}: {keyword}")
                return inst, keyword


# Main function of script.
def main(test: bool, hints_enabled: bool, path: str) -> tuple[str, str]:
    extracted_text = extraction_func(path)
    inst_select, inst_doc = ident_inst(hints_enabled, extracted_text)
    if inst_select == 'Chase':
        if hints_enabled:
            print(f'HINT: {ident_inst}: INSTITUTION FOUND: Chase {inst_doc}')
            print(f'HINT: returning {inst_select}, {inst_doc}')
    elif inst_select == 'SchoolsFirst':
        if hints_enabled:
            print(f'HINT: {ident_inst}: INSTITUTION FOUND: SchoolsFirst {inst_doc}')
            print(f'HINT: returning {inst_select}, {inst_doc}')
    elif inst_select == 'Synchrony':
        if hints_enabled:
            print(f'HINT: {ident_inst}: INSTITUTION FOUND: {inst_doc}')
            print(f'HINT: returning {inst_select}, {inst_doc}')
    elif inst_select == 'PayPal':
        if hints_enabled:
            print(f'HINT: {ident_inst}: INSTITUTION FOUND: {inst_doc}')
            print(f'HINT: returning {inst_select}, {inst_doc}')
    else: # change to elif
        hints_enabled and warnings.warn('Unidentified document presented!')
        return None
    extraction_writing(test, extracted_text)
    return inst_select, inst_doc


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path_1 = 'rep_statements/20240111-statements-1149-.pdf'
    path_2 = 'rep_statements/20240511-statements-1149-.pdf'
    path_3 = 'rep_statements/20240320-statements-9266-.pdf'
    path_4 = 'rep_statements\sfcu-cc-05.pdf'
    path_5 = 'rep_statements\sfcu-ch-05.pdf'
    path_6 = 'rep_statements\synchrony_03.pdf'
    path_7 = 'rep_statements\synchrony_06.pdf'
    path_8 = 'rep_statements\paypal_03.pdf'
    path_9 = 'rep_statements\paypal_11.pdf'
    test_choice = input('Choose path: ')
    try:
        match test_choice:
            case '1':
                main(test, hints_enabled, path_1)
            case '2':
                main(test, hints_enabled, path_2)
            case '3':
                main(test, hints_enabled, path_3)
            case '4':
                main(test, hints_enabled, path_4)
            case '5':
                main(test, hints_enabled, path_5)
            case '6':
                main(test, hints_enabled, path_6)
            case '7':
                main(test, hints_enabled, path_7)
            case '8':
                main(test, hints_enabled, path_8)
            case '9':
                main(test, hints_enabled, path_9)
            case 'q':
                pass
    except NameError as e:
        print('Invalid choice.')