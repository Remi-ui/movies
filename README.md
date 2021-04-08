# movies

About:
aligner.py is a program that aligns the moviescript with the subtitles by using regex and string comparison. The program first divides each subtitle and each part of the script. It then assigns an appropriate tag to the script lines: metadata (M), character (C), dialogue (D), scene boundary (S) and scene description (N). Then it takes the dialogue from the script and removes its tag again, so that it is ready to be compared. After the preprocessing is done, the program takes the dialogue from both the subtitles and the script and aligns them using string comparison.
For a more detailed explanation about the code, you can look at the comments in the programs (aligner.py, subtitles.py and scripts.py)

Preparing to run the program:
Prior to running the program, a few things have to be prepared. First, two files have to be prepared: a SubRip Subtitle file (.srt) containing the subtitles and a standard text file (.txt) containing the script. After this, it is useful to put the files in the same directory, as this will make it easier to call the program.
In order to run the program, you also need a few libraries installed. All the required libraries are in requirements.txt. These can be installed in your terminal by typing: 'pip3 install [LIBRARY]'.

How to run the program:
1. Make sure you have done everything to prepare. (having a .srt and .txt file ready)
2. Call the program in your terminal by typing: 'python3 aligner.py [SUBTITLE_FILE].srt [SCRIPT_FILE].txt', replacing the items in square brackets with your own file names
3. 

