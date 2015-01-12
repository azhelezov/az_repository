"""This is the xrange() function realization"""
def xrange_func(*args):
    i = 0
    if len(args) == 1:
        while abs(i) < abs(args[0]):
            yield i
            i += 1
    elif len(args) == 2:
        i = args[0]
        while abs(i) < abs(args[1]):
            yield i
            i += 1
    elif len(args) == 3:
        i = args[0]
        while abs(i) < abs(args[1]):
            yield i
            i += args[2]

mygenerator = xrange_func(-1, -10, -2)
for i in mygenerator:
    print(i)

