import sys
from fuzzywuzzy import fuzz
import re
import subtitles
import scripts
import jellyfish


def check_input(argv):
    '''
    Handles the input from the user and gives
    an appropriate error if needed
    '''
    if len(argv) == 3:
        if argv[1][-4:-1] + argv[1][-1] != ".srt":
            print("Subtitle file incorrect.")
            exit(-1)
        elif argv[2][-4:-1] + argv[2][-1] != ".txt":
            print("Script file incorrect.")
            exit(-1)
    else:
        print("This program needs exactly two arguments, "
              "please provide a .srt and .txt file.")
        exit(-1)

def clean_script_dialogue(script_list):
    script_dialogue = []
    for element in script_list:
        if element[1] == "D":
            element = re.sub(r'(\(M\)\s\(.*?\))', r'', element)
            script_dialogue.append(element[4:])
    return script_dialogue


def select_dialogue(subtitle_list, script_list):
    """
    Selects the dialogue from the script and the
    subtitles and puts each in their own list
    """
    subtitle_dialogue = []
    i = -1
    # Iterate over the script and subtitles, select only dialogue and
    # append them to a list
    for element in subtitle_list:
        best_match = 0
        best_match_script = ""
        i += 1
        element = element[2]
        for y in range(5):
            if i - 4 >= 0 and len(script_list) - 1 >= i:
                if jellyfish.jaro_winkler_similarity(element, script_list[i - y]) > best_match:
                    best_match = jellyfish.jaro_winkler_similarity(element, script_list[i - y])
                    best_match_script = script_list[i - y]
            elif i + 4 <= len(script_list):
                if jellyfish.jaro_winkler_similarity(element, script_list[i + y]) > best_match:
                    best_match = jellyfish.jaro_winkler_similarity(element, script_list[i + y])
                    best_match_script = script_list[i + y]

        print("Subtitle: ", element, "Script: " ,best_match_script)



def main(argv):
    # Execute scripts.py en subtitles.py vanaf hier.
    check_input(argv)
    subtitle_list = subtitles.main(sys.argv[1])
    script_list = scripts.main(sys.argv[2])
    select_dialogue(subtitle_list, clean_script_dialogue(script_list))


if __name__ == "__main__":
    main(sys.argv)
