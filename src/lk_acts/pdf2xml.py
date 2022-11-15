import os

from lk_acts._utils import log

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
    log.debug(cmd)
    os.system(cmd)
    log.info(f'Converted {pdf_file} (page {page_nos}) into {xml_file}')
