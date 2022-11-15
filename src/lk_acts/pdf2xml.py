import os
import xml.etree.ElementTree as ET

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


def rebuild_text(text):
    assert text.tag == 'text', text.tag
    return text


def rebuild_textline(textline):
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

    font =  list(font_family_to_n.keys())[0]
    size =  list(font_size_to_n.keys())[0]

    class_name = 'normal'
    if 'Bold' in font:
        class_name += '-bold'
    if 'Italic' in font:
        class_name += '-italic'


    new_textline = ET.Element('textline')
    x1, y1, x2, y2 = [str((int)((float)(x))) for x in textline.attrib['bbox'].split(',')]
    new_textline.set('x1', x1)
    new_textline.set('y1', y1)
    new_textline.set('x2', x2)
    new_textline.set('y2', y2)

    new_textline.set('size', size)
    new_textline.set('class_name', class_name)
    new_textline.text = inner_text

    return new_textline


def rebuild_textbox(textbox):
    new_textbox = ET.Element('textbox')
    for textline in textbox:
        new_textbox.append(rebuild_textline(textline))
    return new_textbox


def rebuild_page(page):
    assert page.tag == 'page', page.tag
    new_page = ET.Element('pages')
    for child in page:
        if child.tag == 'textbox':
            new_page.append(rebuild_textbox(child))
    return new_page


def rebuild_pages(pages):
    assert pages.tag == 'pages', pages.tag
    new_pages = ET.Element('pages')
    for page in pages:
        new_pages.append(rebuild_page(page))
    return new_pages


def rebuild(tree):
    new_pages = rebuild_pages(tree.getroot())
    return ET.ElementTree(new_pages)


def convert(pdf_file, page_nos, xml_file):
    raw_xml_file = xml_file[:-4] + '.raw.xml'
    convert_raw(pdf_file, page_nos, raw_xml_file)

    tree = ET.parse(raw_xml_file)
    new_tree = rebuild(tree)

    ET.indent(new_tree, space='  ')
    new_tree.write(xml_file)


if __name__ == '__main__':
    convert(
        pdf_file='data/bill-2022-09-personal-data-protection.pdf',
        page_nos='all',
        xml_file='data/bill-2022-09-personal-data-protection.xml',
    )
