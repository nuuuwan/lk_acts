from utils import www

from lk_acts._utils import log


def convert(url, pdf_file):
    www.download_binary(url, pdf_file)
    log.info(f'Downloaded {url} to {pdf_file}')


if __name__ == '__main__':
    from lk_acts._utils import get_file_name
    from lk_acts.METADATA_LIST import METADATA_LIST

    config = METADATA_LIST[0]
    convert(
        url=config['url'],
        pdf_file=get_file_name(config, 'pdf'),
    )
