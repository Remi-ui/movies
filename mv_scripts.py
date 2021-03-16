import sys

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

def main(argv):
	fname = check_input(argv)
	infile = open(fname, 'r')
	data = infile.read()
	print(data)


# Making the main conditional 
if __name__ == "__main__":
	main(sys.argv)