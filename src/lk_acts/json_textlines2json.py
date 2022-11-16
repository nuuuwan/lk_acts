import re

from utils import JSONFile

from lk_acts._utils import clean_textline, get_file_name, join_textlines, log

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


def extract_intro_data(textlines_with_metadata):
    short_title = ''
    long_title_lines = []
    date_published = None

    for textline in textlines_with_metadata:
        text = clean_textline(textline['text'])
        font_size = (float)(textline['font_size'])
        section_num = textline['section_num']
        if not section_num:
            result = re.match(REGEX_PUBLISHED, text)
            if result:
                date_published = result.groupdict()
            elif 16 < font_size < 17:
                short_title = text.title()
            elif 11 < font_size < 14 and not date_published:
                long_title_lines.append(text)

    long_title = join_textlines(long_title_lines)
    return dict(
        short_title=short_title,
        long_title=long_title,
        date_published=date_published,
    )


def extract_sections(textlines_with_metadata):
    idx = {}
    section_to_marginal_note = {}
    for textline in textlines_with_metadata:
        l1 = textline['section_num']
        l2 = textline['subsection_num']
        l3 = textline['paragraph_num']
        l4 = textline['sub_paragraph_num']

        if l1 not in idx:
            idx[l1] = {}
        if l2 not in idx[l1]:
            idx[l1][l2] = {}
        if l3 not in idx[l1][l2]:
            idx[l1][l2][l3] = {}
        if l4 not in idx[l1][l2][l3]:
            idx[l1][l2][l3][l4] = []

        text = clean_textline(textline['text'])
        if (float)(textline['font_size']) < 9:
            if l1 not in section_to_marginal_note:
                section_to_marginal_note[l1] = []
            section_to_marginal_note[l1].append(text)
        else:
            idx[l1][l2][l3][l4].append(text)

    sections = []
    for l1 in idx:
        l1_textlines = []
        subsections = []

        for l2 in idx[l1]:
            paragraphs = []
            l2_textlines = []

            for l3 in idx[l1][l2]:
                sub_paragraphs = []
                l3_textlines = []
                for l4 in idx[l1][l2][l3]:
                    textlines = idx[l1][l2][l3][l4]
                    if l4:
                        if l1 == 5:
                            print(l1, l2, l3, l4)
                        sub_paragraphs.append(
                            dict(
                                sub_paragraph_num=l4,
                                text=join_textlines(textlines),
                            )
                        )
                    else:
                        l3_textlines += textlines

                if l3:
                    paragraph = dict(
                        paragraph_num=l3,
                        text=join_textlines(l3_textlines),
                    )
                    if sub_paragraphs:
                        paragraph['sub_paragraphs'] = sub_paragraphs
                    paragraphs.append(paragraph)
                else:
                    l2_textlines += l3_textlines
            if l2:
                subsection = dict(
                    subsection_num=l2,
                    text=join_textlines(l2_textlines),
                )
                if paragraphs:
                    subsection['paragraphs'] = paragraphs
                subsections.append(subsection)
            else:
                if len(paragraphs) > 0:
                    subsection = dict(
                        subsection_num="dummy",
                        text="",
                    )
                    subsection['paragraphs'] = paragraphs
                    subsections.append(subsection)
                l1_textlines += l2_textlines

        if l1:
            section = dict(
                section_num=l1,
                marginal_note=join_textlines(
                    section_to_marginal_note.get(l1, '')
                ),
                text=join_textlines(l1_textlines),
                subsections=subsections,
            )
            # assert section['text'].split('.')[0] == str(
            #     section['section_num']
            # ), [
            #     section['text'],
            #     section['section_num'],
            # ]

            if subsections:
                section['subsections'] = subsections

            sections.append(section)
    return sections


def convert(config):
    json_textlines_file = get_file_name(config, 'textlines.json')
    json_file = get_file_name(config, 'json')
    textlines = JSONFile(json_textlines_file).read()
    textlines_with_metadata = add_metadata(textlines)

    intro_data = extract_intro_data(textlines_with_metadata)

    data = intro_data | dict(
        sections=extract_sections(textlines_with_metadata),
    )

    JSONFile(json_file).write(config | data)
    log.info(f'{json_textlines_file} -> {json_file}')
