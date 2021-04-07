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


def combine_multiline(subtitle_list):
    '''
    Combines sublists with multiline dialogue into a single item.
    '''
    for sublist in subtitle_list:
        if len(sublist) == 4:
            sublist[2] = sublist[2] + " " + sublist[3]
            sublist.pop()
    return subtitle_list


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
                element = remove_markup(element.rstrip())
                item.append(element)
            subtitles.append(item)
    return subtitles


def main(subtitle_file):
    subtitle_list = open_subs(subtitle_file)
    return combine_multiline(subtitle_list)


if __name__ == "__main__":
    main(subtitle_file)
