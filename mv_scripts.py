import sys
import re


def check_input(argv):
    '''
    Handles the input from the user and gives
    an appropriate error if needed
    '''
    if len(argv) == 2:
        if argv[1][-4:-1] + argv[1][-1] == ".txt":
            return argv[1]
        else:
            print("This program accepts only txt files, please \
                input one textfile (.txt.gz) as an argument to this program")
            exit(-1)
    else:
        print("This program needs exactly one arguments, \
            please give only one text file as an argument to this program")
        exit(-1)


def split_input(data):
    '''
    Splits the input on two newline characters
    '''
    data_list = re.split(r'\n\n', data)
    return data_list


def filter_character_dialogue(line):
    '''
    Filters on all character names and their dialogue in the script
    cleanlist[0] is always the character
    cleanlist[1] is always the dialogue of that character
    '''
    if re.match(r'([\040]{26})([^\s])', line):
        char_dia = re.split(r'\s{2,}', line[26:], 1)
        cleanlist = []
        for item in char_dia:
            item = re.sub(' +', ' ', item)
            cleanlist.append(item)
        return cleanlist


def filter_scene_boundary(line):
    '''
    Filter all scene boudaries in the script
    '''
    if re.match(r'([\040\n]{5})([^\s])([A-Z \d\W]+$)', line):
        return "(FSB)" + line


def filter_scene_description(line):
    '''
    Filters all scene descriptions out of the script.
    '''
    if re.match(r'(^ {5})([A-z]+)( |\')([a-z]+)', line):
        return "(FSD)" + line


def filter_metadata(line):
    '''
    Filters all metadata out of the script.
    '''
    #If not in the rest, dan is het metadata?
    pass


def label_data(data_list):
    labeled_data = []
    for item in data_list:
        item = item.replace('\n', '')
        if filter_character_dialogue(item) != None:
            item = filter_character_dialogue(item)
            if len(item) == 2:
                labeled_data.append("(C)" + item[0])
                labeled_data.append("D" + item[1])
        elif filter_scene_boundary(item) != None:
            labeled_data.append("(S)" + item)
        elif filter_scene_description(item) != None:
            labeled_data.append("(N)" + item)
        else:
            labeled_data.append("(M)" + item)
    return labeled_data


def main(argv):
    fname = check_input(argv)
    infile = open(fname, 'r')
    data = infile.read()
    data_list = split_input(data)
    labeled_data = label_data(data_list)    


if __name__ == "__main__":
    main(sys.argv)
