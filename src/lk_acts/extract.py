import re

REGEX_CLAUSE = '(?P<clause_num>\\d+)\\.'
REGEX_SUBCLAUSE = '\\((?P<subclause_num>\\d+)\\)\\s.*'
REGEX_PARAGRAPH = '\\((?P<paragraph_num>[ivx]+)\\)\\s.*'
REGEX_SUB_PARAGRAPH = '\\((?P<sub_paragraph_num>[a-z])\\)\\s.*'


def fold_metadata(textlines_with_metadata):
    return textlines_with_metadata


def extract_data(textlines):

    clause_num = None
    subclause_num = None
    paragraph_num = None
    sub_paragraph_num = None
    textlines_with_metadata = []
    for textline in textlines:
        stripped_text = textline['text'].strip()
        if textline['class_name'] == 'normal-bold':
            result = re.match(REGEX_CLAUSE, stripped_text)
            if result:
                clause_num = (int)(result.groupdict()['clause_num'])
                subclause_num = None
                paragraph_num = None
                sub_paragraph_num = None

        if textline['class_name'] == 'normal':
            result = re.match(REGEX_SUBCLAUSE, stripped_text)
            if result:
                subclause_num = (int)(result.groupdict()['subclause_num'])
                paragraph_num = None
                sub_paragraph_num = None

        if textline['class_name'] == 'normal':
            result = re.match(REGEX_PARAGRAPH, stripped_text)
            if result:
                paragraph_num = result.groupdict()['paragraph_num']
                sub_paragraph_num = None

        if textline['class_name'] == 'normal':
            result = re.match(REGEX_SUB_PARAGRAPH, stripped_text)
            if result:
                sub_paragraph_num = result.groupdict()['sub_paragraph_num']

        textlines_with_metadata.append(
            textline
            | dict(
                clause_num=clause_num,
                subclause_num=subclause_num,
                paragraph_num=paragraph_num,
                sub_paragraph_num=sub_paragraph_num,
            )
        )

    fold_metadata(textlines_with_metadata)
    return textlines_with_metadata
