"""This is the realization of "infinite" generator that always gives
out the same value"""
def inf_iterator(value):
    """This function creates an iterator"""
    while True: # infinite cycle
        yield value

print inf_iterator(1).next() # generating a value
