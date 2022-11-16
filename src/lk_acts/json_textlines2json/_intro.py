import re

from lk_acts._utils import clean_textline, join_textlines

REGEX_PUBLISHED = (
    r'\(Published in the Gazette on'
    + r' (?P<month>\w+) (?P<day>\d+), (?P<year>\d{4})\)'
)
REGEX_PRICE = r'Price : Rs. (?P<price_lkr>\d+).00'
REGEX_POSTAGE = r'Postage : Rs. (?P<postage_lkr>\d+).00'


def extract_intro_data(textlines_with_metadata):
    short_title = ''
    long_title_lines = []
    date_published = None
    price_lkr = None
    postage_lkr = None

    for textline in textlines_with_metadata:
        section_num = textline['section_num']
        if section_num:
            break
        text = clean_textline(textline['text'])
        font_size = (float)(textline['font_size'])

        result = re.match(REGEX_PUBLISHED, text)
        if result:
            date_published = result.groupdict()
            continue

        result = re.match(REGEX_PRICE, text)
        if result:
            price_lkr = (int)(result.groupdict()['price_lkr'])
            continue

        result = re.match(REGEX_POSTAGE, text)
        if result:
            postage_lkr = (int)(result.groupdict()['postage_lkr'])
            continue

        if 16 < font_size < 17:
            short_title = text.title()
            continue

        if 11 < font_size < 14 and not date_published:
            long_title_lines.append(text)
            continue

    long_title = join_textlines(long_title_lines)
    return dict(
        short_title=short_title,
        long_title=long_title,
        date_published=date_published,
        price_lkr=price_lkr,
        postage_lkr=postage_lkr,
    )
