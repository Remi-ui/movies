import sys
from itertools import groupby


def open_subs(subtitle_file):
    """This function creates a list containing sublists, that each contain
    three elements: the number, the timestamp and the text."""
    with open("mi.srt", "r", encoding="ISO-8859-1") as f:
        # creates a list with sublists, each containing number, timestamp and
        # text
        subtitle_list = [list(g) for b, g in groupby(f, lambda x:
                                                     bool(x.strip())) if b]
        # creates a new list, with the newline characters removed
        subtitles = []
        for sublist in subtitle_list:
            item = []
            for element in sublist:
                new_element = element.rstrip()
                item.append(new_element)
            subtitles.append(item)
    return subtitles


def main(subtitle_file):
    subtitles = open_subs(subtitle_file)


if __name__ == "__main__":
    main(sys.argv[1])
