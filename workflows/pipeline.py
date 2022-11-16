from src.lk_acts import json2html, pdf2xml, url2pdf, xml2json

if __name__ == '__main__':
    from lk_acts.METADATA_LIST import METADATA_LIST

    for config in METADATA_LIST:
        url2pdf.convert(config)
        pdf2xml.convert(config)
        xml2json.convert(config)
        json2html.convert(config)
