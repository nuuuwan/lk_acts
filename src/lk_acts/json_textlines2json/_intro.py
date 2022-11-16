import re

from lk_acts._utils import clean_textline, join_textlines

REGEX_PUBLISHED = (
    r'\(Published in the Gazette on'
    + r' (?P<month>\w+) (?P<day>\d+), (?P<year>\d{4})\)'
)


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
