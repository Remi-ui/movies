import sys

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


def main(argv):
    # Execute scripts.py en subtitles.py vanaf hier.
    check_input(argv)
    subtitle_list = subtitles.main(sys.argv[1])
    script_list = scripts.main(sys.argv[2])


if __name__ == "__main__":
    main(sys.argv)
