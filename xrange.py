"""This is the xrange() function realization"""
def xrange_func(arg1, arg2=None, arg3=None):
    """This function yelds the values without actually storing them all simultaneously"""
    i = arg1
    if (arg1 != None) and (arg2 == None) and (arg3 == None): # Iterating in positive direction.
        i = 0
        while i < arg1:
            yield i
            i += 1
    elif (arg1 != None) and (arg2 != None) and (arg3 == None): # Iterating in positive direction.
        while i < arg2:
            yield i
            i += 1
    elif (arg1 != None) and (arg2 != None) and (arg3 > 0): # Iterating in positive direction.
        while i < arg2:
            yield i
            i += arg3
    elif (arg1 != None) and (arg2 != None) and (arg3 < 0): # Iterating in negative direction.
        while i > arg2:
            yield i
            i += arg3

def create_list(arg1, arg2=None, arg3=None):
    """This function used to create an example list.
    This list will be used in main() function"""
    example_list = []
    mygenerator = xrange_func(arg1, arg2, arg3) # Creating a generator
    for item in mygenerator: # Generating an example list
        example_list.append(item)
    return example_list

def test(got, expected):
    """Simple function, used in main() to print what each function returns vs.
    what it's supposed to return."""
    if got == expected:
        prefix = ' OK'
    else:
        prefix = ' X'
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))

def main():
    """This is the test of xrange_funcfunction"""
    test(create_list(1, 10, 2), [1, 3, 5, 7, 9])
    test(create_list(1, 6), [1, 2, 3, 4, 5])
    test(create_list(5), [0, 1, 2, 3, 4])
    test(create_list(5, -1, -2), [5, 3, 1])
    test(create_list(-10, -3, 2), [-10, -8, -6, -4])
    test(create_list(-10, -5), [-10, -9, -8, -7, -6])

if __name__ == '__main__':
    main()
