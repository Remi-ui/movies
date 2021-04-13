import subtitles
import scripts
import aligner


subtitle_file = 'mi.srt'
script_file = 'mi.txt'
subtitle_list = subtitles.main(subtitle_file)
script_list = scripts.main(script_file)
cleaned_script = aligner.clean_script_dialogue(script_list)
cleaned_script_norm = []
for item in cleaned_script:
    cleaned_script_norm.append(item[0])
aligned_data = aligner.select_dialogue(subtitle_list, cleaned_script_norm)
pos_count = aligner.find_differences(subtitle_list, cleaned_script_norm)
character_match = aligner.character_dialogue(subtitle_list, script_list, cleaned_script_norm, aligned_data)
timestamped_script = aligner.align_timestamp(cleaned_script, aligned_data, script_list, subtitle_list)


def test_subtitles_main():
    # Format: [['sub number', 'timeframe', 'sub line'], [...]]
    subtitle_list = subtitles.main(subtitle_file)
    assert subtitle_list[3-1][0] == '3'
    assert subtitle_list[9-1][1] == '00:03:00,015 --> 00:03:00,975'
    assert subtitle_list[2-1][2] == 'Come on.'


def test_subtitles_open_subs():
    # Format: [['sub number', 'timeframe', 'sub line'], [...]]
    subtitle_list = subtitles.open_subs(subtitle_file)
    assert subtitle_list[36-1][0] == '36'
    assert subtitle_list[3-1][1] == '00:01:26,839 --> 00:01:29,341'
    assert subtitle_list[9-1][2] == 'We got it.'


def test_subtitles_clean_item():
    test1 = ['4', '00:01:54,366 --> 00:01:55,659', '<i>Za druziye.</i>']
    test2 = ['69', '00:08:42:649 --> 00:08:44:356', '<i>Italic text</i>']
    test3 = ['67', '00:08:34,675 --> 00:08:36:034', 'Did we get it?']
    test4 = ['35', '00:05:25:045 --> 00:05:26:874', 'Normal text']
    result1 = ['4', '00:01:54,366 --> 00:01:55,659', 'Za druziye.']
    result2 = ['69', '00:08:42:649 --> 00:08:44:356', 'Italic text']
    assert subtitles.clean_item(test1) == result1
    assert subtitles.clean_item(test2) == result2
    assert subtitles.clean_item(test3) == test3
    assert subtitles.clean_item('Normal text') == 'Normal text'


def test_split_input():
    # Format: ['line1', 'line2', ...]
    with open(script_file, "r") as infile:
        data = infile.read()
    data_list = scripts.split_input(data)
    assert data_list[36] == '     ANATOLY bends close to KASIMOV. '
    assert data_list[30] == '     ON THE SCREEN '
    assert scripts.split_input('test\n\ntest') == ['test', 'test']


def test_filter_character_dialogue():
    test1 = '                          MAX                Damn!'
    test2 = '     ON THE SCREEN '
    test3 = '                          CHARACTER                Text'
    test4 = '     INT. BUSINESS CAR/TUNNEL - MOVING - DAY '
    result1 = ['MAX', 'Damn!']
    result3 = ['CHARACTER', "Text"]
    assert scripts.filter_character_dialogue(test1) == result1
    assert scripts.filter_character_dialogue(test2) is None
    assert scripts.filter_character_dialogue(test3) == result3
    assert scripts.filter_character_dialogue(test4) is None


def test_filter_scene_boundary():
    test1 = '     INT. PLANE - NIGHT'
    test2 = '     EXT. LONDON PUB - DAY'
    test3 = '     INT. LOCATION - TIME'
    test4 = '     This is not a scene boundary.'
    test5 = '                Stop the train!'
    assert scripts.filter_scene_boundary(test1) == test1
    assert scripts.filter_scene_boundary(test2) == test2
    assert scripts.filter_scene_boundary(test3) == test3
    assert scripts.filter_scene_boundary(test4) is None
    assert scripts.filter_scene_boundary(test5) is None


def test_meta_data_dialogue():
    test1 = '(in English now) Get rid of this scum.'
    test2 = '(Metadata) This is a test.'
    result1 = '(M) (in English now) Get rid of this scum.'
    result2 = '(M) (Metadata) This is a test.'
    assert scripts.filter_meta_data_dialogue(test1) == result1
    assert scripts.filter_meta_data_dialogue(test2) == result2
    assert scripts.filter_meta_data_dialogue('Stop the train! ') is None
    assert scripts.filter_meta_data_dialogue('This is a test') is None


def test_filter_scene_description():
    test1 = '     She then stops before ETHAN.'
    test2 = '     This is a scene description.'
    test3 = '                          ETHAN\n                No, thank you.'
    test4 = '     INT. LOCATION - TIME'
    result1 = ' She then stops before ETHAN.'
    result2 = ' This is a scene description.'
    assert scripts.filter_scene_description(test1) == result1
    assert scripts.filter_scene_description(test2) == result2
    assert scripts.filter_scene_description(test3) is None
    assert scripts.filter_scene_description(test4) is None


def test_filter_meta_data():
    test1 = '     INT. HELICOPTER - DAY'
    test2 = '     EXT. LOCATION - TIME'
    test3 = '     -- AND THE HELICOPTER ROARS RIGHT IN BEHIND IT!'
    test4 = '     -- METADATA'
    test5 = '                Stop the train!'
    assert scripts.filter_meta_data(test1) == test1
    assert scripts.filter_meta_data(test2) == test2
    assert scripts.filter_meta_data(test3) == test3
    assert scripts.filter_meta_data(test4) == test4
    assert scripts.filter_meta_data(test5) is None


def test_label_data():
    # Format: ['(TYPE) line content', ...]
    with open(script_file, "r") as infile:
        data = infile.read()
    data_list = scripts.split_input(data)
    labeled_data = scripts.label_data(data_list)
    assert labeled_data[5-1] == '(S) INT. KIEV APARTMENT - NIGHT'
    assert labeled_data[8-1] == '(M) ON THE SCREEN'
    assert labeled_data[29-1] == '(N) JACK reacts. '
    assert labeled_data[25-1] == '(C) KASIMOV'
    assert labeled_data[26-1] == '(D) You\'re the only one who can help me. '


def test_scripts_main():
    # Format: ['(TYPE) line content', ...]
    labeled_data = scripts.main(script_file)
    assert labeled_data[5-1] == '(S) INT. KIEV APARTMENT - NIGHT'
    assert labeled_data[8-1] == '(M) ON THE SCREEN'
    assert labeled_data[29-1] == '(N) JACK reacts. '
    assert labeled_data[25-1] == '(C) KASIMOV'
    assert labeled_data[26-1] == '(D) You\'re the only one who can help me. '

def test_clean_script_dialogue():
    # Format: [['dialogue line', index], [...]]
    test1 = ['(D) They\'ll kill me. ']
    test2 = ['(D) Did we get it? ']
    test3 = ['(C) KASIMOV']
    result1 = [['They\'ll kill me. ', 0]]
    result2 = [['Did we get it? ', 0]]
    assert aligner.clean_script_dialogue(test1) == result1
    assert aligner.clean_script_dialogue(test2) == result2
    assert aligner.clean_script_dialogue(test3) == []


def test_select_dialogue():
    # Format: [[match value, 'subtitle line', 'script line'], [...]]
    # first line in subtitles
    assert aligned_data[0][1] == 'Come on, come on. She\'s been under too long.'
    # first match
    assert aligned_data[0][2] == 'Jesus, she\'s been under too long. Come on, come on! '
    #first line in script
    assert aligned_data[0][2] != 'Kasimov, Kasimov, good that you called us.'


#def test_default_search_match():
#    test1 = 'Come on, come on. She\'s been under too long.'
#    result1 = 'Jesus, she\'s been under too long. Come on, come on!'
#    assert aligner.default_search_match(test1, script_list, 0, 1)[1] == result1



def test_character_dialogue():
    # Format: ['CHARACTER', 'dialogue match', 'CHARACTER'...]
    # first character in the script
    assert character_match[0] == 'JACK'
    # first subtitle line that matches with the first character's line
    assert character_match[1] == 'Come on, come on. She\'s been under too long.'
    # last character in the script
    assert character_match[-2] == 'FLIGHT ATTENDANT'
    #last subtitle line that matches with the last character's line
    assert character_match[-1] == 'Aruba, perhaps?'


def test_count_pos():
    # Format: {'POS': count}
    test1 = 'This is a test sentence.'
    test2 = 'You\'re the only one who can help me.'
    result1 = {'DT': 2, 'NN': 2, 'VBZ': 1, '.': 1}
    result2 = {'PRP': 2, 'VBP': 1, 'DT': 1, 'JJ': 1, 'NN': 1, 'WP': 1, 'MD': 1, 'VB': 1, '.': 1}
    assert aligner.count_pos(test1) == result1


def test_find_differences():
    # Format: ({key:value}, {key:value})
    assert pos_count == ({'noun': 1413, 'pronoun': 726, 'adj': 404, 'verb': 1382, 'adverb': 371, 'prepos': 530, 'conj': 107}, {'noun': 2028, 'pronoun': 992, 'adj': 674, 'verb': 2030, 'adverb': 530, 'prepos': 767, 'conj': 172})


#def test_align_timestamp():
    #
