import re

REGEX_CLAUSE = r'(?P<clause_num>\d+)\.'
REGEX_SUBCLAUSE = r'\((?P<subclause_num>\d+)\).*'
REGEX_PARAGRAPH = r'\((?P<paragraph_num>[a-z])\).*'
REGEX_SUB_PARAGRAPH = r'\((?P<sub_paragraph_num>[ivx]+)\).*'


def clean_textline(x):
    return x.strip()


def join_textlines(textlines):
    s = ' '.join(textlines)
    s = re.sub('\\s+', ' ', s)
    return s


def cmp_textlines(textline):
    return textline['i_page'] * 1_000_000 - (int)(textline['bbox']['y2'])


def extract_data(textlines_original):
    textlines = sorted(textlines_original, key=cmp_textlines)

    clause_num = None
    subclause_num = None
    paragraph_num = None
    sub_paragraph_num = None
    textlines_with_metadata = []
    for textline in textlines:
        stripped_text = textline['text'].strip()
        x1 = (float)(textline['bbox']['x1'])
        indent = (int)(x1 / 5)

        if textline['class_name'] == 'normal-bold':
            result = re.match(REGEX_CLAUSE, stripped_text)
            if result:
                clause_num = (int)(result.groupdict()['clause_num'])
                subclause_num = None
                paragraph_num = None
                sub_paragraph_num = None

        elif textline['class_name'] == 'normal':
            result = re.match(REGEX_SUBCLAUSE, stripped_text)
            if result:
                subclause_num = (int)(result.groupdict()['subclause_num'])
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
                clause_num=clause_num,
                subclause_num=subclause_num,
                paragraph_num=paragraph_num,
                sub_paragraph_num=sub_paragraph_num,
            )
        )

    clauses = fold_clauses(textlines_with_metadata)
    return dict(
        clauses=clauses,
    )


def fold_clauses(textlines_with_metadata):
    idx = {}
    clause_to_marginal_note = {}
    for textline in textlines_with_metadata:
        l1 = textline['clause_num']
        l2 = textline['subclause_num']
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
            if l1 not in clause_to_marginal_note:
                clause_to_marginal_note[l1] = []
            clause_to_marginal_note[l1].append(text)
        else:
            idx[l1][l2][l3][l4].append(text)

    clauses = []
    for l1 in idx:
        l1_textlines = []
        subclauses = []

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
            if len(paragraphs) > 0 and l2 is None:
                l2 = 'dummy'
            if l2:
                subclause = dict(
                    subclause_num=l2,
                    text=join_textlines(l2_textlines),
                )
                if paragraphs:
                    subclause['paragraphs'] = paragraphs
                subclauses.append(subclause)
            else:
                l1_textlines += l2_textlines

        if l1:
            clause = dict(
                clause_num=l1,
                marginal_note=join_textlines(
                    clause_to_marginal_note.get(l1, '')
                ),
                text=join_textlines(l1_textlines),
                subclauses=subclauses,
            )
            # assert clause['text'].split('.')[0] == str(
            #     clause['clause_num']
            # ), [
            #     clause['text'],
            #     clause['clause_num'],
            # ]

            if subclauses:
                clause['subclauses'] = subclauses

            clauses.append(clause)
    return clauses
