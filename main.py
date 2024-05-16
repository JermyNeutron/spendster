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
def extraction_writing(test,text):
    path = 'temp/temp_scrape.txt' if not test else 'temp/test_temp_scrape.txt'
    with open(path, 'w') as file:
        file.write(text)


# pdf location verification
def loc_ver(test):
    while True:
        pdflink = pdf_drag_drop(test)
        try:
            extracted_text = extraction_func(test,pdflink)
            extraction_writing(test,extracted_text)
            break
        except FileNotFoundError:
            print('File not found. Try again.\n')


if __name__ == '__main__':
    test = True
    loc_ver(test)
    print('program finished')