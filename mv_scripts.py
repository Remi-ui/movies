import sys
import re

def check_input(argv):

    ''' Handles the input from the user and gives
    an appropriate error if needed '''
    if len(argv) == 2:
        # Check if the file is a textfil (.txt.gz)
        if argv[1][-4:-1] + argv[1][-1] == ".txt":
            return argv[1]
        # Give an error message prompting the user to put in a textfile
        else:
            print("This program accepts only txt files, please \
                input one textfile (.txt.gz) as an argument to this program")
            exit(-1)
    # Give an error telling the user that this program only handles one file
    else:
        print("This program needs exactly one arguments, \
            please give only one text file as an argument to this program")
        exit(-1)

def filter_character(line):
	
	''' Filters on all character names in the script '''
	if re.match(r'([\040]{26})([^\s])', line):
		# Add here anything that'd need to happen with the character names
		pass

def filter_scene_boundary(line):
	
	''' Filter all scene descriptions in the script '''
	if re.match(r'([\040]{5})([^\s])([A-Z \d\W]+$)', line):
		#
		# Does not perform perfectly yet, also catches scene descriptions with just capitals on a line
		#
		pass

def main(argv):
	fname = check_input(argv)
	infile = open(fname, 'r')
	data = infile.readlines()
	for line in data:
		filter_character(line)
		filter_scene_boundary(line)


# Making the main conditional 
if __name__ == "__main__":
	main(sys.argv)