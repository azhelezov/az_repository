""" This module is analog to unix utility 'cat' """
import sys


def cat():
    """ This function prints contents of text files """
    for filename in sys.argv[1:]: 
        try: # trying to read files
            fileopened = open(filename, 'r')
        except IOError: # printing a message in case of invalid file name
            print 'cannot open file', filename
        else:
            print fileopened.read() # printing content of each file
            fileopened.close()
cat()
