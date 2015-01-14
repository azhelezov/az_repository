def inf_iterator(value):
    while True:
        yield value

def inf_generator(value):
    return inf_iterator(value).next()
