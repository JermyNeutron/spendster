import sys
import time
import warnings

sys.path.append('.')

import pdfminer
import pdfminer.pdfparser

from functions import inst_pars, chase_sapphire_pref, chase_checking, sfcu_checking, sfcu_inspire, synchrony_car_care, paypal_credit


# PDF file drag and drop prompt.
def pdf_drag_drop(hints_enabled: bool) -> str:
    input_pdflink = input('Drag and drop file here: ')
    # clean input
    if input_pdflink.lower() == 'q': # Exit
        return False
    else:
        pdflink_pos = input_pdflink.lower().find("c")
        if input_pdflink.lower().endswith('\n'):
            pdflink_strstart = input_pdflink[pdflink_pos:-1]
        elif input_pdflink.lower().endswith('\''):
            pdflink_strstart = input_pdflink[pdflink_pos:-1]
        else:
            pdflink_strstart = input_pdflink[pdflink_pos:]
        pdflink = pdflink_strstart.replace('\\', '/')
        # testing purposes
        hints_enabled and print(f"\nHINT: You provided: {pdflink}")
        return pdflink


# PDF location verification and script execution.
def main(test: bool, hints_enabled: bool) -> None:
    print('HINT: Enter \'q\' to quickly end this program!\n\n')
    while True:
        pdflink = pdf_drag_drop(hints_enabled)
        if not pdflink:
            break
        try:
            try:
                institution, document = inst_pars.main(test, hints_enabled, pdflink)
                path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
                with open(path, 'r') as file:
                    uf_text = file.read()
                extracted_text = [item for item in uf_text.split('\n') if item != '']
                # institution-specific analysis
                if institution == 'Chase':
                    if document == 'Sapphire Preferred': # Chase CC
                        hints_enabled and print(chase_sapphire_pref)
                        chase_sapphire_pref.main(test, hints_enabled, extracted_text)
                        hints_enabled and print(f"HINT: program resetting...")
                        time.sleep(2)
                    elif document == 'Chase debit': # Chase Checking
                        hints_enabled and print(chase_checking)
                        chase_checking.main(test, hints_enabled, extracted_text)
                        hints_enabled and print(f"HINT: program resetting...")
                        time.sleep(2)
                elif institution == 'SchoolsFirst': # SFCU CC
                    if document == 'www.SchoolsFirstFcu.org':
                        sfcu_inspire.main(test, hints_enabled, extracted_text)
                        hints_enabled and print(f"HINT: program resetting...")
                        time.sleep(2)
                    elif document == 'www.SchoolsFirstfcu.org': # SFCU Checking
                        sfcu_checking.main(test, hints_enabled, uf_text)
                        hints_enabled and print(f"HINT: program resetting...")
                        time.sleep(2)
                elif institution == 'Synchrony': # Synchrony
                    synchrony_car_care.main(test, hints_enabled, extracted_text)
                    hints_enabled and print(f"HINT: program resetting...")
                    time.sleep(2)
                elif institution == 'PayPal': # PayPal
                    paypal_credit.main(test, hints_enabled, extracted_text)
                    hints_enabled and print(f"HINT: program resetting...")
                    time.sleep(2)
                else:
                    print('Institution or statement not supported.\nPlease submit an issue and we\'ll get right to it.')
            except pdfminer.pdfparser.PDFSyntaxError as e:
                print('File not found. Try again.\n')
        except FileNotFoundError:
            print('File not found. Try again.\n')


if __name__ == '__main__':
    test = True
    hints_enabled = True
    main(test, hints_enabled)


'''
Commit Comments:
- 

'''