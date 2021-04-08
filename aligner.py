import sys
import re
import subtitles
import scripts
import jellyfish
import nltk
from nltk.tokenize import sent_tokenize


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
            # remove metadata
            element = re.sub(r'(\(M\)\s\(.*?\))', r'', element)
            element = element[4:]
            # there are more than 2 sentences, break them up (easier to stringmatch with this)

            if len(sent_tokenize(element)) > 2:
                splitted_element = (sent_tokenize(element))
                for element in splitted_element:
                    if len(splitted_element) > 2:
                        element = element + " " + splitted_element[1]
                        script_dialogue.append(element)
                        splitted_element = splitted_element[2:]
                    else:
                        script_dialogue.append(element)
            script_dialogue.append(element)
    return script_dialogue

def default_search_match(element, script_list, i, ratio):
    best_match = 0
    best_match_script = ""
    # Have the range in which the subtitle will search for a match be dependent on the ratio 
    # between the length of the list of the script and the length of the subtitle list
    ratio = 15 * ratio
    if int(ratio) < 15:
        ratio = 15
    for y in range(int(ratio)):
        if i - y >= 0:
            # print(y, "score: ", jellyfish.jaro_winkler_similarity(element, script_list[i - y]), "subtitle: ", element, "script: " ,script_list[i - y])
            if jellyfish.jaro_winkler_similarity(element, script_list[i - y]) > best_match:
                best_match = jellyfish.jaro_winkler_similarity(element, script_list[i - y])
                best_match_script = script_list[i - y]
        if i + y < len(script_list):
            # print(y,"score: ", jellyfish.jaro_winkler_similarity(element, script_list[i + y]), "subtitle: ", element, "script: " ,script_list[i + y])
            if jellyfish.jaro_winkler_similarity(element, script_list[i + y]) > best_match:
                best_match = jellyfish.jaro_winkler_similarity(element, script_list[i + y])
                best_match_script = script_list[i + y]
    return best_match, best_match_script

def select_dialogue(subtitle_list, script_list):
    """
    Selects the dialogue from the script and the
    subtitles and puts each in their own list
    """
    best_match = 0
    best_match_script = ""
    i = -1
    # Iterate over the script and subtitles, select only dialogue and
    # append them to a list
    
    # print(len(subtitle_list))
    # print(len(script_list))
    for element in subtitle_list:
        i += 1
        el_list = element
        # clean HTML 5 markup
        element = subtitles.clean_item(element)
        element = element[2]
        if best_match > 0.9 and len(subtitle_list) > 1:
            script_list = script_list[script_list.index(best_match_script) + 1:]
            subtitle_list = subtitle_list[subtitle_list.index(el_list) + 1:]
            i = 0
            best_match, best_match_script = default_search_match(element, script_list, i, len(script_list) / len(subtitle_list))
        else: 
            best_match, best_match_script = default_search_match(element, script_list, i, len(script_list) / len(subtitle_list))
        
        print("Score: ", best_match,"Subtitle: ", element, "Script: " ,best_match_script)



def main(argv):
    # Execute scripts.py en subtitles.py vanaf hier.
    check_input(argv)
    subtitle_list = subtitles.main(sys.argv[1])
    script_list = scripts.main(sys.argv[2])
    select_dialogue(subtitle_list, clean_script_dialogue(script_list))


if __name__ == "__main__":
    main(sys.argv)
