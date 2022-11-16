import re

from utils import JSONFile

from lk_acts._utils import get_file_name, log
from lk_acts.json_textlines2json._intro import extract_intro_data
from lk_acts.json_textlines2json._sections import extract_sections

REGEX_SECTION = r'(?P<section_num>\d+)\.'
REGEX_SUBSECTION = r'\((?P<subsection_num>\d+)\).*'
REGEX_PARAGRAPH = r'\((?P<paragraph_num>[a-z])\).*'
REGEX_SUB_PARAGRAPH = r'\((?P<sub_paragraph_num>[ivx]+)\).*'
REGEX_PUBLISHED = (
    r'\(Published in the Gazette on'
    + r' (?P<month>\w+) (?P<day>\d+), (?P<year>\d{4})\)'
)


def cmp_textlines(textline):
    return textline['i_page'] * 1_000_000 - (int)(textline['bbox']['y2'])


def add_metadata(textlines_original):
    textlines = sorted(textlines_original, key=cmp_textlines)

    section_num = None
    subsection_num = None
    paragraph_num = None
    sub_paragraph_num = None
    textlines_with_metadata = []
    for textline in textlines:
        stripped_text = textline['text'].strip()
        x1 = (float)(textline['bbox']['x1'])
        indent = (int)(x1 / 5)

        if textline['class_name'] == 'normal-bold':
            result = re.match(REGEX_SECTION, stripped_text)
            if result:
                section_num = (int)(result.groupdict()['section_num'])
                subsection_num = None
                paragraph_num = None
                sub_paragraph_num = None

        elif textline['class_name'] == 'normal':
            result = re.match(REGEX_SUBSECTION, stripped_text)
            if result:
                subsection_num = (int)(result.groupdict()['subsection_num'])
                paragraph_num = None
                sub_paragraph_num = None
            else:
                result = re.match(REGEX_PARAGRAPH, stripped_text)
                if result and indent < 39:
                    paragraph_num = result.groupdict()['paragraph_num']
                    sub_paragraph_num = None
                else:
                    result = re.match(REGEX_SUB_PARAGRAPH, stripped_text)
                    if result:
                        sub_paragraph_num = result.groupdict()[
                            'sub_paragraph_num'
                        ]

        textlines_with_metadata.append(
            textline
            | dict(
                section_num=section_num,
                subsection_num=subsection_num,
                paragraph_num=paragraph_num,
                sub_paragraph_num=sub_paragraph_num,
            )
        )

    return textlines_with_metadata


def convert(config):
    json_textlines_file = get_file_name(config, 'textlines.json')
    json_file = get_file_name(config, 'json')
    textlines = JSONFile(json_textlines_file).read()
    textlines_with_metadata = add_metadata(textlines)

    textlines_with_metadata_file = get_file_name(
        config, 'textlines_with_metadata.json'
    )
    JSONFile(textlines_with_metadata_file).write(textlines_with_metadata)

    intro_data = extract_intro_data(textlines_with_metadata)

    data = intro_data | dict(
        sections=extract_sections(textlines_with_metadata),
    )

    JSONFile(json_file).write(config | data)
    log.info(f'{json_textlines_file} -> {json_file}')
