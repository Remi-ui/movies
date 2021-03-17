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

def split_input(data):

	''' Splits the input on two newline characters '''
	data_list = re.split(r'\n\n',data)
	return data_list

def filter_character_dialogue(line):
	
	''' Filters on all character names and their dialogue in the script
		cleanlist[0] is always the character
		cleanlist[1] is always the dialogue of that character
	'''
	if re.match(r'([\040]{26})([^\s])', line):
		char_dia = re.split(r'\s{2,}', line[26:], 1)
		cleanlist = []
		for item in char_dia:
			item = re.sub(' +', ' ', item)
			cleanlist.append(item)

def filter_scene_boundary(line):
	
	''' Filter all scene boudaries in the script '''
	if re.match(r'([\040\n]{5})([^\s])([A-Z \d\W]+$)', line):
		# Add here anything that'd need to happen with the scene boundaries
		pass

def main(argv):
	fname = check_input(argv)
	infile = open(fname, 'r')
	data = infile.read()
	data_list = split_input(data)
	for item in data_list:
		item = item.replace('\n', '')
		filter_character_dialogue(item)
		filter_scene_boundary(item)


# Making the main conditional 
if __name__ == "__main__":
	main(sys.argv)