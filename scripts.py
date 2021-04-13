# File name: scripts.py
# Authors: Kylian de Rooij, Robert van Timmeren, Remi Thüss
# Description: A program that'll label movie scripts
# and returns the full labelled script.

import sys
import re


def split_input(data):
    '''
    Splits the input on two newline characters
    '''
    data_list = re.split(r'\n\n', data)
    return data_list


def split_character_dialogue(line, spaces):
    '''
    Splits the character from its dialogue and returns a list to the
    function filter_character_dialogue
    '''
    char_dia = re.split(r'\s{2,}', line[spaces:], 1)
    cleanlist = []
    for item in char_dia:
        cleanlist.append(item)
    return cleanlist


def filter_character_dialogue(line):
    '''
    Filters on all character names and their dialogue in the script
    cleanlist[0] is always the character
    cleanlist[1] is always the dialogue of that character
    '''
    if re.match(r'([\040]{26})([^\s])', line):
        return split_character_dialogue(line, 26)
    elif re.match(r'([\040]{37})([^\s])', line):
        return split_character_dialogue(line, 37)


def filter_scene_boundary(line):
    '''
    Filter all scene boudaries in the script
    '''
    if re.match(r'([\040\n]{5})(INT\.|EXT\.)([A-Z \d\W]+$)', line):
        return line
    elif re.match(r'([\040\n]{15})(INT\.|EXT\.)([A-Z \d\W]+$)', line):
        return line


def filter_scene_description(line):
    '''
    Filters all scene descriptions out of the script.
    '''
    if re.match(r'(^ {5})([A-z]+)( |\')([a-z]+)', line):
        return re.sub(' +', ' ', line)
    elif re.match(r'(^ {15})([A-z]+)( |\')([a-z]+)', line):
        return re.sub(' +', ' ', line)


def filter_meta_data_dialogue(full_dia):
    '''
    Filters all meta data from the dialogue and returns a list of meta data
    '''
    data_list = []
    if re.findall(r'(\(.*?\))', full_dia):
        dialogue = re.sub(r'(\(.*?\))', r'(M) \1', full_dia)
        return dialogue


def filter_meta_data(line):
    '''
    Filters all metadata that isn't in the dialogue
    '''
    if re.match(r'([\040\n]{5})([^\s])([A-Z \d\W]+$)', line):
        return line
    elif re.match(r'([\040\n]{15})([^\s])([A-Z \d\W]+$)', line):
        return line
    elif re.match(r'([\040\n]+)([^\s])([A-Z \d\W]+$)', line):
        return line


def label_data(data_list):
    labeled_data = []
    for item in data_list:
        item = item.replace('\n', '')
        if filter_character_dialogue(item) is not None:
            item = filter_character_dialogue(item)
            if len(item) == 2:
                labeled_data.append("(C) " + re.sub(' +', ' ', item[0]))
                if filter_meta_data_dialogue(item[1]) is not None:
                    dia = filter_meta_data_dialogue(item[1])
                    labeled_data.append("(D) " + re.sub(' +', ' ', dia))
                else:
                    labeled_data.append("(D) " + re.sub(' +', ' ', item[1]))
        elif filter_scene_boundary(item) is not None:
            labeled_data.append("(S)" + re.sub(' +', ' ', item))
        elif filter_scene_description(item) is not None:
            labeled_data.append("(N)" + re.sub(' +', ' ', item))
        elif filter_meta_data(item) is not None:
            labeled_data.append("(M)" + re.sub(' +', ' ', item))
    return labeled_data


def main(script_file):
    with open(script_file, 'r', encoding='ISO-8859-1') as infile:
        data = infile.read()
    data_list = split_input(data)
    labeled_data = label_data(data_list)
    return labeled_data


if __name__ == "__main__":
    main(script_file)
