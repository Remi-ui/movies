import sys
from itertools import groupby


def remove_markup(new_element):
    '''
    Removes HTML5 subtitle markup language from elements.
    '''
    if new_element[:3] == '<i>' and new_element[-4:] == '</i>':
        return new_element[3:-4]
    else:
        return new_element


def open_subs(subtitle_file):
    '''
    This function creates a list containing sublists, that each contain
    three elements: the number, the timestamp and the text.
    '''
    with open(subtitle_file, 'r', encoding='ISO-8859-1') as f:
        # creates a list with sublists, each containing number, timestamp and
        # text
        subtitle_list = [list(g) for b, g in groupby(f, lambda x:
                                                     bool(x.strip())) if b]
        # creates a new list, with the newline characters removed
        subtitles = []
        for sublist in subtitle_list:
            item = []
            for element in sublist:
                element = remove_markup(element.rstrip())
                item.append(element)
            subtitles.append(item)
    return subtitles


def main(subtitle_file):
    return open_subs(subtitle_file)


if __name__ == '__main__':
    main(subtitle_file)
