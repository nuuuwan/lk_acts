import os

PY_BIN = 'python3'
BIN = '/Library/Frameworks/Python.framework/Versions/3.10/bin/pdf2txt.py'


def convert(pdf_file, page_nos, xml_file):
    cmd = ' '.join(
        [
            f'{PY_BIN} {BIN}',
            f'-o {xml_file}',
            f'-p {page_nos}' if page_nos != 'all' else '',
            pdf_file,
        ]
    )
    os.system(cmd)


if __name__ == '__main__':
    convert(
        pdf_file='data/bill-2022-09-personal-data-protection.pdf',
        page_nos='all',
        xml_file='data/bill-2022-09-personal-data-protection.xml',
    )
