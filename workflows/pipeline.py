from src.lk_acts import (json2html, json_textlines2json, pdf2xml, url2pdf,
                         xml2json_textlines)


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
    run_post_xml()
