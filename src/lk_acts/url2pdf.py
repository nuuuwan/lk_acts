from utils import www

from lk_acts._utils import get_file_name, log


def convert(config):
    url = config['url']
    pdf_file = get_file_name(config, 'pdf')
    www.download_binary(url, pdf_file)
    log.info(f'{url} -> {pdf_file}')
