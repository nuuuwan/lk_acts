import os
import xml.etree.ElementTree as ET

from utils import JSONFile

PY_BIN = 'python3'
BIN = '/Library/Frameworks/Python.framework/Versions/3.10/bin/pdf2txt.py'


def convert_raw(pdf_file, page_nos, raw_xml_file):
    cmd = ' '.join(
        [
            f'{PY_BIN} {BIN}',
            f'-o {raw_xml_file}',
            f'-p {page_nos}' if page_nos != 'all' else '',
            pdf_file,
        ]
    )
    os.system(cmd)


def parse_text(text):
    assert text.tag == 'text', text.tag
    return text


def parse_textline(textline):
    font_family_to_n = {}
    font_size_to_n = {}
    inner_text = ''
    for text in textline:
        font_size = text.attrib.get('size')
        font_family = text.attrib.get('font')
        font_family_to_n[font_family] = (
            font_family_to_n.get(font_family, 0) + 1
        )
        font_size_to_n[font_size] = font_size_to_n.get(font_size, 0) + 1
        inner_text += text.text

    font = list(font_family_to_n.keys())[0]
    size = list(font_size_to_n.keys())[0]

    class_name = 'normal'
    if 'Bold' in font:
        class_name += '-bold'
    if 'Italic' in font:
        class_name += '-italic'

    x1, y1, x2, y2 = [
        str((int)((float)(x))) for x in textline.attrib['bbox'].split(',')
    ]

    return dict(
        font_size=size,
        class_name=class_name,
        bbox=dict(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        ),
        text=inner_text,
    )


def is_valid_textline(data_textline):
    stripped_text = data_textline['text'].strip()
    x1 = (int)(data_textline['bbox']['x1'])
    indent = (int)(x1 / 10)
    if indent == 22 and stripped_text == 'Personal Data Protection':
        return False

    if indent in [13, 14] and stripped_text in ['5', '10', '15', '20', '25', '30']:
        return False

    if indent in [15, 39] and len(stripped_text) <= 3:
        return False

    return True

def parse_textbox(textbox):
    textlines = []
    for textline in textbox:
        data_textline = parse_textline(textline)
        if valid_textline(data_textline):
            textlines.append(data_textline)
    return textlines


def parse_page(i_page, page):
    assert page.tag == 'page', page.tag
    textlines = []
    for child in page:
        if child.tag == 'textbox':
            textlines += parse_textbox(child)
    return dict(
        page_num=i_page + 1,
        textlines=textlines,
    )


def parse_pages(pages):
    assert pages.tag == 'pages', pages.tag
    data_pages = []
    for i_page, page in enumerate(pages):
        data_pages.append(parse_page(i_page, page))
    return dict(
        pages=data_pages,
    )


def parse(tree):
    return parse_pages(tree.getroot())


def convert(xml_file, json_file):
    data = parse(ET.parse(xml_file))
    JSONFile(json_file).write(data)


if __name__ == '__main__':
    convert(
        xml_file='data/bill-2022-09-personal-data-protection.xml',
        json_file='data/bill-2022-09-personal-data-protection.json',
    )
