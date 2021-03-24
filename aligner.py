import sys
from fuzzywuzzy import fuzz

import subtitles
import scripts


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


def select_dialogue(subtitle_list, script_list):
    """
    Selects the dialogue from the script and the
    subtitles and puts each in their own list
    """
    script_dialogue = []
    subtitle_dialogue = []
    # Iterate over the script and subtitles, select only dialogue and
    # append them to a list
    for element in script_list:
        if element[1] == "D":
            script_dialogue.append(element[4:])
    for element in subtitle_list:
        subtitle_dialogue.append(element[2])
    return subtitle_dialogue, script_dialogue


def main(argv):
    # Execute scripts.py en subtitles.py vanaf hier.
    check_input(argv)
    subtitle_list = subtitles.main(sys.argv[1])
    script_list = scripts.main(sys.argv[2])
    subtitle_dialogue, script_dialogue = select_dialogue(subtitle_list, script_list)


if __name__ == "__main__":
    main(sys.argv)
