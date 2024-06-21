import sys
import time

sys.path.append('.')

import pdfminer
import pdfminer.pdfparser

from functions import inst_pars, chase_sapphire_pref, chase_checking


# PDF file drag and drop prompt.
def pdf_drag_drop(hints_enabled):
    input_pdflink = input('Drag and drop file here: ')
    # clean input
    if input_pdflink.lower() == 'q':
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
        if hints_enabled:
            print(f"\nHINT: You provided: {pdflink}")
        return pdflink


# PDF location verification and script execution.
def main(test, hints_enabled):
    while True:
        pdflink = pdf_drag_drop(hints_enabled)
        if not pdflink:
            break
        try:
            try:
                institution, document = inst_pars.main(test, hints_enabled, pdflink)
                path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
                with open(path, 'r') as file:
                    text = file.read()
                extracted_text = [item for item in text.split('\n') if item != '']
                # institution-specific analysis
                if institution == 'Chase':
                    if document == 'Sapphire Preferred':
                        if hints_enabled:
                            print(chase_sapphire_pref)
                        chase_sapphire_pref.main(test, hints_enabled, extracted_text)
                        if hints_enabled:
                            print(f"HINT: program sleeping...")
                        time.sleep(3)
                        return False
                    if document == 'Chase debit':
                        if hints_enabled:
                            print(chase_checking)
                        chase_checking.main(test, hints_enabled, extracted_text)
                        if hints_enabled:
                            print(f"HINT: program sleeping...")
                        time.sleep(3)
                        return False
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