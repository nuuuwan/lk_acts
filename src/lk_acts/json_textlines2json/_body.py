from lk_acts._utils import clean_textline, join_textlines


def extract_parts(textlines_with_metadata):
    idx = {}
    section_to_marginal_note = {}
    for textline in textlines_with_metadata:
        if textline['schedule_num']:
            break
        l0 = textline['part_num']
        l1 = textline['section_num']
        l2 = textline['subsection_num']
        l3 = textline['paragraph_num']
        l4 = textline['sub_paragraph_num']

        if l0 not in idx:
            idx[l0] = {}
        if l1 not in idx[l0]:
            idx[l0][l1] = {}
        if l2 not in idx[l0][l1]:
            idx[l0][l1][l2] = {}
        if l3 not in idx[l0][l1][l2]:
            idx[l0][l1][l2][l3] = {}
        if l4 not in idx[l0][l1][l2][l3]:
            idx[l0][l1][l2][l3][l4] = []

        text = clean_textline(textline['text'])
        if (float)(textline['font_size']) < 9:
            if l1 not in section_to_marginal_note:
                section_to_marginal_note[l1] = []
            section_to_marginal_note[l1].append(text)
        else:
            idx[l0][l1][l2][l3][l4].append(text)

    parts = []
    for l0 in idx:
        l0_textlines = []
        sections = []

        for l1 in idx[l0]:
            l1_textlines = []
            subsections = []

            for l2 in idx[l0][l1]:
                paragraphs = []
                l2_textlines = []

                for l3 in idx[l0][l1][l2]:
                    sub_paragraphs = []
                    l3_textlines = []
                    for l4 in idx[l0][l1][l2][l3]:
                        textlines = idx[l0][l1][l2][l3][l4]
                        if l4:
                            if l1 == 5:
                                print(l1, l2, l3, l4)
                            sub_paragraphs.append(
                                dict(
                                    sub_paragraph_num=l4,
                                    textlines=textlines,
                                )
                            )
                        else:
                            l3_textlines += textlines

                    if l3:
                        paragraph = dict(
                            paragraph_num=l3,
                            textlines=l3_textlines,
                        )
                        if sub_paragraphs:
                            paragraph['sub_paragraphs'] = sub_paragraphs
                        paragraphs.append(paragraph)
                    else:
                        l2_textlines += l3_textlines
                if l2:
                    subsection = dict(
                        subsection_num=l2,
                        textlines=l2_textlines,
                    )
                    if paragraphs:
                        subsection['paragraphs'] = paragraphs
                    subsections.append(subsection)
                else:
                    if len(paragraphs) > 0:
                        subsection = dict(
                            subsection_num="dummy",
                            textlines=[],
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
                    textlines=l1_textlines,
                    subsections=subsections,
                )
                sections.append(section)
        if l0 or l1:
            part = dict(
                part_num=l0, textlines=l0_textlines, sections=sections
            )
            parts.append(part)
    return parts
