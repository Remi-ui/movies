import sys
from fuzzywuzzy import fuzz
import re
import subtitles
import scripts

from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import string


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


def preprocess_data(line):
    stop_words = stopwords.words('english')
    line = ''.join([word for word in line if word not in string.punctuation])
    line = line.lower()
    line = ' '.join([word for word in line.split() if word not in stop_words])
    return line
    

def align_subtitle_script(preprocessed_subtitles, preprocessed_script):
    aligned_subtitle_script = preprocessed_subtitles[0:1] + preprocessed_script[0:9]
    vectorizer = CountVectorizer().fit_transform(aligned_subtitle_script)
    vectors = vectorizer.toarray()

    highest_vector = 0
    index = 0
    for i in range(9):
        i += 1
        if cos_sim_vectors(vectors[0], vectors[i]) > highest_vector:
            highest_vector = cos_sim_vectors(vectors[0], vectors[i])
            index = i
    print("subtitle: ", aligned_subtitle_script[0], "| script: ", aligned_subtitle_script[i], "| accuracy: ", round(highest_vector, 3))


def cos_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def main(argv):
    # Executes scripts.py and subtitles.py and stores their return in variables.
    check_input(argv)
    subtitle_list = subtitles.main(sys.argv[1])
    script_list = scripts.main(sys.argv[2])

    # Preprocess data and store in new variables.
    preprocessed_subtitles = []
    preprocessed_script = []
    for line in subtitle_list:
        preprocessed_subtitles.append(preprocess_data(line[2]))
    for line in script_list:
        if line[:3] == "(D)":
            preprocessed_script.append(preprocess_data(line[4:]))

    # Align subtitles and script
    align_subtitle_script(preprocessed_subtitles, preprocessed_script)


if __name__ == "__main__":
    main(sys.argv)
