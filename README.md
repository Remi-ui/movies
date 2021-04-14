# Aligner for movie scripts and subtitles

<h2>About</h2>
aligner.py is a program that aligns the moviescript with the subtitles by using regex and string comparison. The program first divides each subtitle and each part of the script. It then assigns an appropriate tag to the script lines: metadata (M), character (C), dialogue (D), scene boundary (S) and scene description (N). Then it takes the dialogue from the script and removes its tag again, so that it is ready to be compared. After the preprocessing is done, the program takes the dialogue from both the subtitles and the script and aligns them using string comparison.
For a more detailed explanation about the code, you can look at the comments in the programs (aligner.py, subtitles.py and scripts.py)

<h2>Preparing to run the program</h2>
Prior to running the program, a few things have to be prepared. First, two files have to be prepared: a SubRip Subtitle file (.srt) containing the subtitles and a standard text file (.txt) containing the script. After this, it is useful to put the files in the same directory, as this will make it easier to call the program.
In order to run the program, you also need a few libraries installed. All the required libraries are in requirements.txt. These can be installed in your terminal by typing: 'pip3 install [LIBRARY]'.

<h2>How to run the program</h2>
<ol>
<li>Make sure you have done everything to prepare. (having a .srt and .txt file ready)</li>
<li>Call the program in your terminal by typing: 'python3 aligner.py [SUBTITLE_FILE].srt [SCRIPT_FILE].txt', replacing the items in square brackets with your own file names. The files we based our results (listed below) on can be found in this repository.</li>
<li>Follow the instructions given by the terminal interface</li>
<li></li>
<li></li>
</ol>

<h2>Notable results</h2>

To illustrate the performance of the program the first 100 matches of 4 movies were annotated by hand to check if the program found the right match.
The results were:

- Mission impossible: 32 correct, 68 incorrect
- The assignment: 63 correct, 37 incorrect
- Birthday girl: 31 correct, 69 incorrect
- Chinatown: 89 correct, 11 incorrect

Total: 215 correct, 185 incorrect
Accuracy based on results above: 53.75%

If you'd like to reproduce these results follow these steps:
<ol>
<li>Open aligner.py and uncomment the last print statement in the select_dialogue function.</li>
<li>Run the program as normally using the script and subtitle (provided in the scripts_subtitles folder) for the desired movie</li>
<li>Compare as you wish! These raw results will be exactly the same as the ones we used for the annotation as well as the raw results below</li>
</ol>

Raw results: https://docs.google.com/spreadsheets/d/1vUpw906vSVXqh4vc2DsbTovbaMD9jZwdd3C7rRKSZC8/edit#gid=0

<h2>Other important information</h2>

It is important to note that that the program will not work on all scripts as the regex required to make this work is different for many scripts.
The regex implemented in this program allows for 2 different types of scripts which'll allow for handling the most common types of scripts to be handled.
We tested this on 16 different scripts out of which the programm will work on 12 of them. 

The 12 scripts the program works on:
1. Mission impossible
2. The assignment
3. Birthday girl
4. Chinatown
5. Mystery Men
6. Intolerable cruelty
7. Crash+(1996)
8. The Cooler
9. Confidence
10. Cold Mountain
11. Autumn in New York
12. 84 Charlie Mopic

The 4 scripts the program didn't work on:
1. 8mm
2. The Fifth Element
3. Carnivore
4. The Cable Guy

A summary of the differences between the scripts listed above can be found here: https://docs.google.com/document/d/1rBSFIQtOgTlFwx307YCkwJkS6_ezAEBf5Gh1HtDDLkk/edit?ts=60742cab

<h2>Research question</h2>

<b>Subtitles contain less nouns than their respective scripts<b>

To answer the hypothesis the scripts and subtitles for 10 different movies were POS-tagged. In total subtitles contained 495610 words and the subtitles contained 615655 words.
The subtitles contained 19147 nouns and the scripts contained 24968 nouns, which means that 3.86% of the subtitles were nouns and 4.06% of the scripts were nouns. It therefore seems that subtitles contain less nouns than the scripts.
The earlier described hypothesis can therefore be accepted.

Raw data: https://docs.google.com/spreadsheets/d/150YQtX-zg8Dtcm1p6E7EqZWD-_9SMR_BxGRO5A01eA4/edit?usp=sharing 

<h2>Who did what</h2>

<b>Robert</b>
- Interface
- Output in JSON
- Movie annotation
- Add timestap from subtitle to script
- Testing how NLTK works
- Label function
- Combining scripts.py and subtitles.py output

<b>Kylian</b>
- Pytests
- First part of README
- Requirements.txt
- Research question
- Movie annotation
- Summirization of differences between script and subtitle using NLTK
- Overview of regex required for different scripts
- Add regex to be able to label more scripts

<b>Remi</b>
- Movie annotation (x2)
- Add character name to subtitles
- Aligner itself
- Second part of README
- Code cleanup for pytest
- Splitting up functions for better readability
- Label function