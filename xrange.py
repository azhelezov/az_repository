"""This is the xrange() function realization"""
def xrange_func(start, stop=None, step=None):
    """This function yelds the values without actually storing them all simultaneously"""
    i = start
    if (stop is None) and (step is None): # Iterating in positive direction.
        i = 0
        while i < start:
            yield i
            i += 1
    elif (stop is not None) and (step is None): # Iterating in positive direction.
        while i < stop:
            yield i
            i += 1
    elif (stop is not None) and (step > 0): # Iterating in positive direction.
        while i < stop:
            yield i
            i += step
    elif (stop is not None) and (step < 0): # Iterating in negative direction.
        while i > stop:
            yield i
            i += step

def create_list(start, stop=None, step=None):
    """This function used to create an example list.
    This list will be used in main() function"""
    example_list = []
    mygenerator = xrange_func(start, stop, step) # Creating a generator
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
