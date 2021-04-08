import sys
from itertools import groupby


def clean_item(item):
    '''
    Combines multiline sublists into one and removes HTML5 markup language.
    '''
    if len(item) == 4:
        item[2] = item[2] + " " + item[3]
        item.pop()
    if item[2][:3] == '<i>' and item[2][-4:] == '</i>':
        item[2] = item[2][3:-4]
    return item


def open_subs(subtitle_file):
    """This function creates a list containing sublists, that each contain
    three elements: the number, the timestamp and the text."""
    with open(subtitle_file, "r", encoding="ISO-8859-1") as f:
        subtitle_list = [list(g) for b, g in groupby(f, lambda x:
                                                     bool(x.strip())) if b]
        subtitles = []
        for sublist in subtitle_list:
            item = []
            for element in sublist:
                element = element.rstrip()
                item.append(element)
            item = clean_item(item)
            subtitles.append(item)
    return subtitles


def main(subtitle_file):
    return open_subs(subtitle_file)


if __name__ == "__main__":
    main(subtitle_file)
