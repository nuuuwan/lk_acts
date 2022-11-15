import os

from utils import www

from lk_acts._constants import DIR_DATA
from lk_acts._utils import log


def get_file(label):
    return os.path.join(DIR_DATA, f'{label}.pdf')


def download_bill(url, label):
    doc_file = get_file(label)
    www.download_binary(url, doc_file)
    log.info(f'Downloaded {url} to {doc_file}')


if __name__ == '__main__':
    download_bill(
        'http://documents.gov.lk/files/bill/2022/1/167-2022_E.pdf',
        'bill-2022-09-personal-data-protection',
    )
