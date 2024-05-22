import sys
from functions import inst_pars, chase_sapphire_pref

sys.path.append('.')


# PDF file drag and drop prompt.
def pdf_drag_drop(test):
    input_pdflink = input('Drag and drop file here: ')
    # clean input
    if input_pdflink.lower() == 'q':
        return False
    else:
        pdflink_pos = input_pdflink.lower().find("c")
        pdflink_strstart = input_pdflink[pdflink_pos:-1]
        pdflink = pdflink_strstart.replace('\\', '/')
        # testing purposes
        if test:
            print(f"TEST: You provided: {pdflink}")
        return pdflink


# PDF location verification and script execution.
def main(test):
    while True:
        pdflink = pdf_drag_drop(test)
        if not pdflink:
            break
        try:
            institution = inst_pars.main(test, pdflink)
            path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
            with open(path, 'r') as file:
                extracted_text = file.read()
            # institution-specific analysis
            if institution == 'Chase':
                chase_sapphire_pref.main(test, extracted_text)
                return False
            else:
                print('Institution or statement not supported.\nPlease submit an issue and we\'ll get right to it.')
        except FileNotFoundError:
            print('File not found. Try again.\n')


if __name__ == '__main__':
    test = True
    main(test)