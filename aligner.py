# File name: Aligner.py
# Authors: Kylian de Rooij, Robert van Timmeren, Remi Thüss
# Description: A program that'll align movie scripts with subtitles

import sys
import re
import csv
import json

import subtitles
import scripts
import jellyfish
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag

from fuzzy_match import match
from fuzzy_match import algorithims
from fuzzywuzzy import fuzz
from collections import Counter


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
    ''' This function cleans up the list containing everything from the scripts
    to then return only the dialogue and the index of that dialogue '''

    script_dialogue = []
    index = 0
    for element in script_list:
        if element[1] == "D":
            # remove metadata
            element = re.sub(r'(\(M\)\s\(.*?\))', r'', element)
            element = element[4:]
            if len(sent_tokenize(element)) > 2:
                splitted_element = (sent_tokenize(element))
                for element in splitted_element:
                    if len(splitted_element) > 2:
                        element = element + " " + splitted_element[1]
                        script_dialogue.append([element, index])
                        splitted_element = splitted_element[2:]
                    else:
                        script_dialogue.append([element, index])
            script_dialogue.append([element, index])
        index += 1
    return script_dialogue


def alternative_search(element, script_list, best_match, best_match_script, i):
    ''' This function using Jaro Winkler similarity
    will be used if NLTK doesn't find a sufficiently good match.
    Overall this improves accuracy. '''
    bm = best_match
    for a in range(15):
        if i - a >= 0:
            if jellyfish.jaro_winkler_similarity(element,
               script_list[i - a]) > bm:
                bm = jellyfish.jaro_winkler_similarity(element,
                                                       script_list[i - a])
                best_match_script = script_list[i - a]
        if i + a < len(script_list):
            if jellyfish.jaro_winkler_similarity(element,
               script_list[i + a]) > bm:
                bm = jellyfish.jaro_winkler_similarity(element,
                                                       script_list[i + a])
                best_match_script = script_list[i + a]
    return bm, best_match_script


def default_search_match(element, script_list, i, ratio):
    ''' This function searches for a match between
    the subtitle and script using NLTK by default
    and the Jaro Winkler similarity if NLTK gives a low score'''

    best_match = 0
    best_match_script = ""
    # Have the range in which the subtitle will search for a match be
    # dependent on the ratio between the length of the list of the script
    # and the length of the subtitle list
    ratio = 20 * ratio
    if int(ratio) < 20:
        ratio = 20
    for y in range(int(ratio)):
        if i - y >= 0:
            if algorithims.cosine(element, script_list[i - y]) > best_match:
                best_match = algorithims.cosine(element, script_list[i - y])
                best_match_script = script_list[i - y]
        if i + y < len(script_list):
            if algorithims.cosine(element, script_list[i + y]) > best_match:
                best_match = algorithims.cosine(element, script_list[i + y])
                best_match_script = script_list[i + y]
    if best_match < 0.35:
        best_match, best_match_script = alternative_search(element,
                                                           script_list,
                                                           best_match,
                                                           best_match_script,
                                                           i)
    return best_match, best_match_script


def select_dialogue(subtitle_list, script_list):
    """
    Selects the dialogue from the script and the
    subtitles and puts each in their own list
    """
    best_match = 0
    best_match_script = ""
    results = []
    i = -1
    for element in subtitle_list:
        i += 1
        el_list = element
        element = element[2]
        ratio = len(script_list) / len(subtitle_list)
        if best_match > 0.9 and len(subtitle_list) > 1:
            script_list = script_list[script_list.index(best_match_script):]
            subtitle_list = subtitle_list[subtitle_list.index(el_list):]
            i = 0
            best_match, best_match_script = default_search_match(element,
                                                                 script_list,
                                                                 i,
                                                                 ratio)
        else:
            best_match, best_match_script = default_search_match(element,
                                                                 script_list,
                                                                 i,
                                                                 ratio)
        results.append([best_match, element, best_match_script])
    return results


def character_dialogue(subtitle_list, script_list,
                       cleaned_script_norm, aligned_data):
    ''' This functions adds the character name
    to the subtitles based on the script '''
    character_dialogue = []
    for match in aligned_data:
        sub = match[1]
        script = match[2]
        indices = [i for i, s in enumerate(script_list) if script in s]
        for i in indices:
            character_dialogue.append(script_list[i - 1][4:])
            character_dialogue.append(sub)
    return character_dialogue


def count_pos(text):
    '''
    This function takes a string and counts each part of speech in the string.
    The output is in the form of a dictionary (pos: count).
    '''
    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    pos_count = Counter(tag for word, tag in tagged)
    return pos_count


def find_differences(subtitle_list, cleaned_script_norm):
    ''' This function finds differences between
    the scripts and subtitles using POS tags '''
    subtitle_dialogue = ''
    script_dialogue = ''
    for item in subtitle_list:
        subtitle_dialogue += re.sub(' +', ' ', item[2] + ' ')
    script_dia_list = cleaned_script_norm
    for item in script_dia_list:
        script_dialogue += re.sub(' +', ' ', item + ' ')

    # Creates dictionaries with POS for subtitles and script
    # Format: {'POS': count}
    # Keys: 'noun', 'pronoun', 'adj', 'verb', 'adverb', 'prepos', 'conj
    sub_pos = count_pos(subtitle_dialogue)
    sub_count = {}
    sub_count['wc'] = len(subtitle_dialogue)
    sub_count['noun'] = sub_pos['NN'] + sub_pos['NNS']
    sub_count['pronoun'] = sub_pos['PRP'] + sub_pos['PRP$']
    sub_count['adj'] = sub_pos['JJ'] + sub_pos['JJR'] + sub_pos['JJS']
    sub_count['verb'] = sub_pos['VB'] + sub_pos['VBG'] + sub_pos['VBD'] +\
        sub_pos['VBN'] + sub_pos['VBP'] + sub_pos['VBZ']
    sub_count['adverb'] = sub_pos['RB'] + sub_pos['RBR'] + sub_pos['RBS']
    sub_count['prepos'] = sub_pos['IN']
    sub_count['conj'] = sub_pos['CC']

    scr_pos = count_pos(script_dialogue)
    scr_count = {}
    scr_count['wc'] = len(script_dialogue)
    scr_count['noun'] = scr_pos['NN'] + scr_pos['NNS']
    scr_count['pronoun'] = scr_pos['PRP'] + scr_pos['PRP$']
    scr_count['adj'] = scr_pos['JJ'] + scr_pos['JJR'] + scr_pos['JJS']
    scr_count['verb'] = scr_pos['VB'] + scr_pos['VBG'] +\
        scr_pos['VBD'] + scr_pos['VBN'] + scr_pos['VBP'] + scr_pos['VBZ']
    scr_count['adverb'] = scr_pos['RB'] + scr_pos['RBR'] + scr_pos['RBS']
    scr_count['prepos'] = scr_pos['IN']
    scr_count['conj'] = scr_pos['CC']

    return sub_count, scr_count


def align_timestamp(cleaned_script, aligned_data, script_list, subtitle_list):
    '''This function places a timestamp in the script.'''
    i = 0
    for element in aligned_data:
        for element2 in cleaned_script:
            if element2[0] == element[2]:
                aligned_data[i].append(element2[1])
        i += 1
    for element in aligned_data:
        script_list[element[3]] += "(T) " + str(subtitle_list[0][1])
        subtitle_list.pop(0)
    return script_list
