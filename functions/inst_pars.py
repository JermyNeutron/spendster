# Institution Parser
from pdfminer.high_level import extract_text as pdfmextract_text


'''Supported Institutions and Statements
- Chase Sapphire Preferred
'''
list_institutions = ['Chase Mobile']
ident_Chase = ['Chase Mobile', 'Sapphire Preferred', 'Sapphire Reserved', 'Chase']

# extract text
def extraction_func(path):
    text = pdfmextract_text(path)
    return text


# write extracted text to temp file
def extraction_writing(test, text):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'w') as file:
        file.write(text)


# parse text to identify institution
def ident_inst(extracted_text):
    for inst in list_institutions:
        if inst in extracted_text:
            return inst


def main(test, path):
    extracted_text = extraction_func(path)
    institution = ident_inst(extracted_text)
    if institution in ident_Chase:
        if test:
            print(f'TEST: {ident_inst}: INSTITUTION FOUND: {institution}')
        inst_return =  "Chase"
    extraction_writing(test, extracted_text)
    return inst_return


if __name__ == '__main__':
    test = True
    path = 'rep_statements/20240111-statements-1149-.pdf'
    institution = main(test, path)
    if institution in ident_Chase:
        print('This document belongs to Chase Bank')
    else:
        print('wtf is this?!')