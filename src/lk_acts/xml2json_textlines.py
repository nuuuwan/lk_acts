import os
import xml.etree.ElementTree as ET

from utils import JSONFile

from lk_acts._utils import get_file_name, log

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


def parse_textline(i_page, textline):
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
        i_page=i_page,
        bbox=dict(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        ),
        font_size=size,
        class_name=class_name,
        text=inner_text,
    )


def is_valid_textline(data_textline):
    stripped_text = data_textline['text'].strip()
    x1 = (int)(data_textline['bbox']['x1'])
    indent = (int)(x1 / 10)
    if indent == 22 and stripped_text == 'Personal Data Protection':
        return False

    if indent in [13, 14] and stripped_text in [
        '5',
        '10',
        '15',
        '20',
        '25',
        '30',
    ]:
        return False

    if indent in [15, 39] and len(stripped_text) <= 3:
        return False

    return True


def parse_textbox(i_page, textbox):
    textlines = []
    for textline in textbox:
        data_textline = parse_textline(i_page, textline)
        if is_valid_textline(data_textline):
            textlines.append(data_textline)
    return textlines


def parse_page(i_page, page):
    assert page.tag == 'page', page.tag
    textlines = []
    for child in page:
        if child.tag == 'textbox':
            textlines += parse_textbox(i_page, child)
    return textlines


def parse_pages(pages):
    assert pages.tag == 'pages', pages.tag
    textlines = []
    for i_page, page in enumerate(pages):
        textlines += parse_page(i_page, page)

    return textlines


def convert(config):
    xml_file = get_file_name(config, 'xml')
    json_textlines_file = get_file_name(config, 'textlines.json')

    tree = ET.parse(xml_file)
    textlines = parse_pages(tree.getroot())

    JSONFile(json_textlines_file).write(textlines)
    log.info(f'{xml_file} -> {json_textlines_file}')
