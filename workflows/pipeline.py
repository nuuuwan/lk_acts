import sys

from src.lk_acts import json2html, pdf2xml, url2pdf, xml2json_textlines
from src.lk_acts.json_textlines2json import json_textlines2json


def run_all():
    from lk_acts.METADATA_LIST import METADATA_LIST

    for config in METADATA_LIST:
        url2pdf.convert(config)
        pdf2xml.convert(config)
        xml2json_textlines.convert(config)
        json_textlines2json.convert(config)
        json2html.convert(config)


def run_post_xml():
    from lk_acts.METADATA_LIST import METADATA_LIST

    for config in METADATA_LIST:
        json_textlines2json.convert(config)
        json2html.convert(config)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        run_all()
    else:
        run_post_xml()
