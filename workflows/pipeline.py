from src.lk_acts import (json2html, json_textlines2json, pdf2xml, url2pdf,
                         xml2json_textlines)

if __name__ == '__main__':
    from lk_acts.METADATA_LIST import METADATA_LIST

    for config in METADATA_LIST:
        url2pdf.convert(config)
        pdf2xml.convert(config)
        xml2json_textlines.convert(config)
        json_textlines2json.convert(config)
        json2html.convert(config)
