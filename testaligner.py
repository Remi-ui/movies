import subtitles
import scripts
import aligner


subtitle_file = 'mi.srt'
script_file = 'mi.txt'


def test_subtitles_main():
    subtitle_list = subtitles.main(subtitle_file)
    assert subtitle_list[3-1][0] == '3'
    assert subtitle_list[9-1][1] == '00:03:00,015 --> 00:03:00,975'
    assert subtitle_list[2-1][2] == 'Come on.'


def test_subtitles_open_subs():
    subtitle_list = subtitles.open_subs(subtitle_file)
    assert subtitle_list[36-1][0] == '36'
    assert subtitle_list[3-1][1] == '00:01:26,839 --> 00:01:29,341'
    assert subtitle_list[9-1][2] == 'We got it.'


def test_subtitles_remove_markup():
    assert subtitles.remove_markup('<i>Za druziye.</i>') == 'Za druziye.'
    assert subtitles.remove_markup('<i>Italic text</i>') == 'Italic text'
    assert subtitles.remove_markup('Did we get it?') == 'Did we get it?'
    assert subtitles.remove_markup('Normal text') == 'Normal text'


def test_split_input():
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
    assert scripts.filter_scene_description(test1) == test1
    assert scripts.filter_scene_description(test2) == test2
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
    with open(script_file, "r") as infile:
        data = infile.read()
    data_list = scripts.split_input(data)
    labeled_data = scripts.label_data(data_list)
    assert labeled_data[2-1] == '(S)      INT. KIEV APARTMENT - NIGHT'
    assert labeled_data[5-1] == '(M)      ON THE SCREEN'
    assert labeled_data[26-1] == '(N)      JACK reacts. '
    assert labeled_data[22-1] == '(C) KASIMOV'
    assert labeled_data[23-1] == '(D) You\'re the only one who can help me. '


def test_scripts_main():
    labeled_data = scripts.main(script_file)
    assert labeled_data[2-1] == '(S)      INT. KIEV APARTMENT - NIGHT'
    assert labeled_data[5-1] == '(M)      ON THE SCREEN'
    assert labeled_data[26-1] == '(N)      JACK reacts. '
    assert labeled_data[22-1] == '(C) KASIMOV'
    assert labeled_data[23-1] == '(D) You\'re the only one who can help me. '

def test_clean_script_dialogue():
    test1 = ['(D) They\'ll kill me. ']
    test2 = ['(D) Did we get it? ']
    test3 = ['(C) KASIMOV']
    result1 = ['They\'ll kill me. ']
    result2 = ['Did we get it? ']
    assert aligner.clean_script_dialogue(test1) == result1
    assert aligner.clean_script_dialogue(test2) == result2
    assert aligner.clean_script_dialogue(test3) == []


#def test_select_dialogue():
    #Finish when program is finished


#def test_aligner_main():
    #Finish when program is finished
