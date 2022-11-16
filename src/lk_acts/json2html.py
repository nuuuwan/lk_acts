from utils import JSONFile
from utils.xmlx import _

from lk_acts._utils import get_file_name, log

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
    return _(
        'p',
        indent_str + textline['text'],
        dict(
            style=';'.join(
                list(
                    map(
                        lambda x: '%s:%s' % (x[0], x[1]),
                        style.items(),
                    )
                )
            )
        ),
    )


def render_sub_paragraph(sub_paragraph):
    return _(
        'div',
        [
            _('div', sub_paragraph['text'], {'class': 'sub_paragraph-text'}),
        ],
        {'class': 'sub-paragraph'},
    )


def render_paragraph(paragraph):
    return _(
        'div',
        [
            _('div', paragraph['text'], {'class': 'paragraph-text'}),
        ]
        + [
            render_sub_paragraph(sub_paragraph)
            for sub_paragraph in paragraph.get('sub_paragraphs', [])
        ],
        {'class': 'paragraph'},
    )


def render_subsection(subsection):
    return _(
        'div',
        [
            _('div', subsection['text'], {'class': 'subsection-text'}),
        ]
        + [
            render_paragraph(paragraph)
            for paragraph in subsection.get('paragraphs', [])
        ],
        {'class': 'subsection'},
    )


def render_section(section):
    return _(
        'tr',
        [
            _(
                'td',
                [
                    _(
                        'div',
                        [
                            _(
                                'div',
                                section['text'],
                                {'class': 'section-text'},
                            ),
                        ]
                        + [
                            render_subsection(subsection)
                            for subsection in section['subsections']
                        ],
                        {'class': 'section-body'},
                    ),
                ],
            ),
            _(
                'td',
                section['marginal_note'],
                {'class': 'section-marginal-note'},
            ),
        ],
        {'class': 'section'},
    )


def render_sections(sections):
    return _(
        'table',
        [_('tbody', [render_section(section) for section in sections])],
        {'class': 'sections'},
    )


def convert(config):
    json_file = get_file_name(config, 'json')
    html_file = get_file_name(config, 'html')

    data = JSONFile(json_file).read()

    html = _(
        'html',
        [
            _(
                'head',
                [
                    _(
                        'link',
                        None,
                        dict(rel="stylesheet", href="../styles.css"),
                    ),
                ],
            ),
            _(
                'body',
                [
                    _(
                        'div',
                        'Democratic Socialist Republic of Sri Lanka',
                        {'class': 'title-kicker'},
                    ),
                    _('h1', data['name'], {'class': 'title'}),
                    _(
                        'h2',
                        'No. %d of %d' % (data['num'], data['year']),
                        {'class': 'sub-title'},
                    ),
                    render_sections(data['sections']),
                ],
            ),
        ],
        {},
    )
    html.store(html_file)
    log.info(f'{json_file} -> {html_file}')
