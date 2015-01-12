""" This module is analog to unix utility 'cat' """
import sys
def cat():
    """ This function prints contents of text files """
    args = sys.argv[1:] # reading all file names
    for filename in args: # printing content of each file
        fileopened = open(filename, 'r')
        text = fileopened.read()
        print text
cat()
