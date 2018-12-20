#!/usr/bin/env python
import argparse

# find object
#
class find(object):

    # __init__
    # class initialization
    #
    def __init__(self):
        pass

    # find_word()
    # get a keyword and print line to a specific file
    #
    def find_word(self, word, input, output):

        # Open the file with read only permition
        f = open(input)
        # Open the file with writting permition
        o = open(output,"w+")

        # use readline() to read the first line 
        line = f.readline()

        # use the read line to read further.
        # If the file is not empty keep reading one line
        # at a time, till the file is empty
        while line:
            if word in line :
                # in python 3 print is a builtin function, so
                print(line)
                # in python 2+
                # print line
                
                # write into output file
                o.write(line)
                
            # use realine() to read next line
            line = f.readline()

        # close files
        f.close()
        o.close()

# The main function will parse arguments via the parser variable.  These
# arguments will be defined by the user on the console.  This will pass
# the word argument the user wants to parse along with the filename the
# user wants to use, and also provide help text if the user does not 
# correctly pass the arguments.
if __name__ == "__main__":

    options = argparse.ArgumentParser()
    options.add_argument('-w', '--word', default='OptimiSME2G', type=str, help='word to find')
    options.add_argument('-i', '--input', default='log.txt', type=str, help='Log file')
    options.add_argument('-o', '--output', default='output.txt', type=str, help='Output file')
    args = options.parse_args()

    # find function: 
    # example: --word OptimiSME2G -i log.txt -o result.txt
    #
    if args.word != "":   
        print 'Keyword: ' + args.word + '\n'
        print 'Input: ' + args.input + '\n'
        print 'Output: ' + args.output + '\n'
 
        key = find()
        key.find_word(args.word, args.input, args.output)
