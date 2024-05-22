import sys
from functions import inst_pars, chase_sapphire_pref

sys.path.append('.')


# pdf filedrop prompt
def pdf_drag_drop(test):
    input_pdflink = input('Drag and drop file here: ')
    # clean input
    pdflink_pos = input_pdflink.find("c")
    pdflink_strstart = input_pdflink[pdflink_pos:-1]
    pdflink = pdflink_strstart.replace('\\', '/')
    # testing purposes
    if test:
        print(f"TEST: You provided: {pdflink}")
    return pdflink


# pdf location verification
def main(test):
    while True:
        pdflink = pdf_drag_drop(test)
        try:
            institution = inst_pars.main(test, pdflink)
            path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
            with open(path, 'r') as file:
                extracted_text = file.read()
            # institution-specific analysis
            if institution == 'Chase':
                chase_sapphire_pref.main(test, extracted_text)
            return False
        except FileNotFoundError:
            print('File not found. Try again.\n')


if __name__ == '__main__':
    test = True
    main(test)