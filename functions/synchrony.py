# Synchrony

import sys
sys.path.append('.')

from functions.inst_pars import extraction_func, extraction_writing


def keyphrase_search(hints_enabled: bool, extracted_text: list) -> str:
    pass


def main():
    pass


if __name__ == '__main__':
    test = True
    hints_enabled = True
    path = 'rep_statements/synchrony_03.pdf'
    # path = 'rep_statements/synchrony_05.pdf'
    # path = 'rep_statements/synchrony_06.pdf'
    uf_text = extraction_func(path)
    extraction_writing(test, uf_text)

    main()