import os

from lk_acts._utils import get_file_name, log

PY_BIN = 'python3'
BIN = '/Library/Frameworks/Python.framework/Versions/3.10/bin/pdf2txt.py'


def convert(config):
    pdf_file = get_file_name(config, 'pdf')
    page_nos = 'all'
    xml_file = get_file_name(config, 'xml')
    cmd = ' '.join(
        [
            f'{PY_BIN} {BIN}',
            f'-o {xml_file}',
            f'-p {page_nos}' if page_nos != 'all' else '',
            pdf_file,
        ]
    )
    os.system(cmd)
    log.info(f'{pdf_file} ({page_nos}) -> {xml_file}')
