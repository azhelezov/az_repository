""" This module is analog to unix utility 'cat' """
import sys


def cat():
    """ This function prints contents of text files """
    if len(sys.argv[1:]) == 0: #user input is empty check
        print 'There are no files selected'
    for filename in sys.argv[1:]:
        try: # trying to read files
            fileopened = open(filename, 'r')
        except IOError: # printing a message in case of invalid file name
            print 'Cannot open file', filename
        else:
            print fileopened.read() # printing content of each file
            fileopened.close()
cat()
