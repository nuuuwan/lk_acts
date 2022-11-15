import os

from lk_acts._utils import log

PY_BIN = 'python3'
BIN = '/Library/Frameworks/Python.framework/Versions/3.10/bin/pdf2txt.py'


def convert(pdf_file, page_no, xml_file):
    cmd = f'{PY_BIN} {BIN} -o {xml_file} -p {page_no} {pdf_file} '
    log.debug(cmd)
    os.system(cmd)
    log.info(f'Converted {pdf_file} (page {page_no}) into {xml_file}')
