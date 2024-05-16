from pdfminer.high_level import extract_text


# pdf filedrop prompt
def pdf_drag_drop(test):
    input_pdflink = input('Drag and drop file here: ')
    # clean input
    pdflink_pos = input_pdflink.find("c")
    pdflink_strstart = input_pdflink[pdflink_pos:-1]
    pdflink = pdflink_strstart.replace('\\', '/')

    # testing purposes
    if test:
        print(f"TEST: You provided: {pdflink}\n")

    return pdflink


# pdf text scraper
def extraction_func(test,pdf_path):
    text = extract_text(pdf_path)
    return text


# writes and store extracted text
def extraction_writing(test, text):

    with open('temp/temp_scrape.txt', 'w') as file:
        file.write(text)


if __name__ == '__main__':
    test = True
    pdflink = pdf_drag_drop(test)
    extracted_text = extraction_func(test,pdflink)
    extraction_writing(test,extracted_text)