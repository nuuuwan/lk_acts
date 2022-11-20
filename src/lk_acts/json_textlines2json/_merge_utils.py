from lk_acts._utils import clean_textline


def merge_textlines(textlines):
    return list(
        map(
            lambda textline: clean_textline(textline['text']),
            textlines,
        )
    )
