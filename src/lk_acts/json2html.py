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
            _(
                'div',
                render_lines(sub_paragraph['textlines']),
                {'class': 'sub_paragraph-text'},
            ),
        ],
        {'class': 'sub-paragraph'},
    )


def render_paragraph(paragraph):
    return _(
        'div',
        [
            _(
                'div',
                render_lines(paragraph['textlines']),
                {'class': 'paragraph-text'},
            ),
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
            _(
                'div',
                render_lines(subsection['textlines']),
                {'class': 'subsection-text'},
            ),
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
                                render_lines(section['textlines']),
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


def render_part(part):
    return _(
        'div',
        [
            _('h3', render_lines(part['textlines']), {'class': 'part-title'}),
            render_sections(part['sections']),
        ],
        {'class': 'part'},
    )


def render_parts(parts):
    return _(
        'div',
        [render_part(part) for part in parts],
        {'class': 'parts'},
    )


def render_schedule(schedule):
    return _(
        'div',
        [
            _(
                'h3',
                render_lines(schedule['textlines']),
                {'class': 'schedule-title'},
            ),
            render_sections(schedule['sections']),
        ],
        {'class': 'schedule'},
    )


def render_schedules(schedules):
    return _(
        'div',
        [render_schedule(schedule) for schedule in schedules],
        {'class': 'schedules'},
    )


def render_lines(lines):
    return list(
        map(
            lambda line: _('p', line),
            lines,
        )
    )


def render_intro(data):
    date_published_str = '(Published in the Gazette on %s %s, %s)' % (
        data['date_published']['month'],
        data['date_published']['day'],
        data['date_published']['year'],
    )

    return _(
        'div',
        [
            _('h1', data['short_title'], {'class': 'short-title'}),
            _(
                'div',
                render_lines(data['long_title_lines']),
                {'class': 'long-title'},
            ),
            _(
                'p',
                render_lines(data['presented_by_lines']),
                {'class': 'presented-by'},
            ),
            _('p', date_published_str, {'class': 'date-published'}),
            _('h3', 'Preamble', {'class': 'preamble-title'}),
            _(
                'p',
                render_lines(data['preamble_lines']),
                {'class': 'preamble'},
            ),
        ],
        {'class': 'intro'},
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
                    render_intro(data),
                    render_parts(data['parts']),
                    render_schedules(data['schedules']),
                ],
            ),
        ],
        {},
    )
    html.store(html_file)
    log.info(f'{json_file} -> {html_file}')
