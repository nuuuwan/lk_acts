import os
import xml.etree.ElementTree as ET

from utils import JSONFile
from utils.xmlx import _

PY_BIN = 'python3'
BIN = '/Library/Frameworks/Python.framework/Versions/3.10/bin/pdf2txt.py'

def render_textline(textline):
    style = {}
    style['font_size'] = textline['font_size']
    if textline['class_name'] == 'normal-bold':
        style['font-weight'] = 'bold'
    if textline['class_name'] == 'normal-italic':
        style['font-style'] = 'italic'
    x1 = (int)(textline['bbox']['x1'])
    indent = (int)(x1 / 10)
    indent_str = f'[{indent}]' + ('-' * indent)
    return _('p', indent_str + textline['text'], dict(style=';'.join(
        list(map(
            lambda x: '%s:%s' % (x[0], x[1]),
            style.items(),
        ))
    )))

def render_page(page):
    rendered_inner_list = []
    textlines = []
    for textline in page['textlines']:
        textlines.append(textline)

    sorted_textlines = sorted(
        textlines,
        key=lambda textline: -(int)(textline['bbox']['y1']),
    )


    return _('div',  [render_textline(textline) for textline in sorted_textlines] + [_('hr')], {'class': 'page'})


def render_pages(pages):
    return _('div', [render_page(page) for page in pages], {'class': 'pages'})


def convert(json_file, html_file):
    data = JSONFile(json_file).read()
    html = _('html', [render_pages(data['pages'])], {})
    html.store(html_file)


if __name__ == '__main__':
    convert(
        json_file='data/bill-2022-09-personal-data-protection.json',
        html_file='data/bill-2022-09-personal-data-protection.html',
    )
