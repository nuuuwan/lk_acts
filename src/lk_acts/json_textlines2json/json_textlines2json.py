import re

from utils import JSONFile

from lk_acts._utils import get_file_name, log
from lk_acts.json_textlines2json._intro import extract_intro_data
from lk_acts.json_textlines2json._parts import extract_parts
from lk_acts.json_textlines2json._schedules import extract_schedules

REGEX_PART = r'PART (?P<part_num>[IVX]+)'
REGEX_SECTION = r'(?P<section_num>\d+)\.'
REGEX_SUBSECTION = r'\((?P<subsection_num>\d+)\).*'
REGEX_PARAGRAPH = r'\((?P<paragraph_num>[a-z])\).*'
REGEX_SUB_PARAGRAPH = r'\((?P<sub_paragraph_num>[ivx]+)\).*'
REGEX_SCHEDULE = r'SCHEDULE (?P<schedule_num>[IVX]+)'


def cmp_textlines(textline):
    return textline['i_page'] * 1_000_000 - (int)(textline['bbox']['y2'])


def add_metadata(textlines_original):
    textlines = sorted(textlines_original, key=cmp_textlines)

    schedule_num = None
    part_num = None
    section_num = None
    subsection_num = None
    paragraph_num = None
    sub_paragraph_num = None
    textlines_with_metadata = []
    prev_paragraph_num = None
    for textline in textlines:
        stripped_text = textline['text'].strip()

        result = re.match(REGEX_PART, stripped_text)
        if result:
            part_num = result.groupdict()['part_num']
            section_num = None
            subsection_num = None
            paragraph_num = None
            sub_paragraph_num = None

        result = re.match(REGEX_SCHEDULE, stripped_text)
        if result:
            schedule_num = result.groupdict()['schedule_num']
            section_num = None
            subsection_num = None
            paragraph_num = None
            sub_paragraph_num = None

        result = re.match(REGEX_SECTION, stripped_text)
        if result:
            section_num = (int)(result.groupdict()['section_num'])
            subsection_num = None
            paragraph_num = None
            sub_paragraph_num = None

        if textline['class_name'] == 'normal':
            result = re.match(REGEX_SUBSECTION, stripped_text)
            if result:
                subsection_num = (int)(result.groupdict()['subsection_num'])
                paragraph_num = None
                sub_paragraph_num = None
            else:
                result = re.match(REGEX_PARAGRAPH, stripped_text)
                found_paragraph = False
                if result:
                    paragraph_num_candidate = result.groupdict()[
                        'paragraph_num'
                    ]
                    if (
                        paragraph_num_candidate != 'i'
                        or prev_paragraph_num == 'h'
                    ):
                        paragraph_num = paragraph_num_candidate
                        sub_paragraph_num = None
                        prev_paragraph_num = paragraph_num
                        found_paragraph = True

                if not found_paragraph:
                    result = re.match(REGEX_SUB_PARAGRAPH, stripped_text)
                    if result:
                        sub_paragraph_num = result.groupdict()[
                            'sub_paragraph_num'
                        ]

        textlines_with_metadata.append(
            textline
            | dict(
                part_num=part_num,
                schedule_num=schedule_num,
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
        parts=extract_parts(textlines_with_metadata),
        schedules=extract_schedules(textlines_with_metadata),
    )

    JSONFile(json_file).write(config | data)
    log.info(f'{json_textlines_file} -> {json_file}')
