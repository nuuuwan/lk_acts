from lk_acts._utils import clean_textline, join_textlines

MIN_GAP = 10


def merge_textlines(textlines):
    grouped_texts = []
    current_text_lines = []
    prev_y1 = None
    for textline in textlines:
        bbox = textline['bbox']
        y1 = (float)(bbox['y1'])
        y2 = (float)(bbox['y2'])
        text = clean_textline(textline['text'])

        if all([prev_y1 and prev_y1 - y2 > MIN_GAP]):
            grouped_texts.append(join_textlines(current_text_lines))
            current_text_lines = []
        current_text_lines.append(text)

        prev_y1 = y1

    if current_text_lines:
        grouped_texts.append(join_textlines(current_text_lines))

    return grouped_texts
