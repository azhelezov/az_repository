"""This is the xrange() function realization"""
import unittest


def xrange_func(start, stop=None, step=1):
    """This function used to create an example list.
    This list will be used in main() function"""
    current = 0 if stop is None else start # If stop is not provided then iterate from 0 to start
    final = stop if stop else start
    """ If step is less than 0 then we need to increment while current value
    is greather than final, i.e. we are approaching final from the left
    Example (5, -1, -2) => [5,3,1]
    Otherwise current should be less than final, i.e. we are approaching
    final from the right
    Example (5) => [0,1,2,3,4]"""
    compare = (lambda x, y: x < y) if step > 0 else (lambda x, y: x > y)
    while compare(current, final): # Actual generator
        yield current
        current += step

def create_list(start, stop=None, step=1):
    """Simple function, used to test the xrange_func"""
    gen = xrange_func(start, stop, step) # creating a generator using xrange_func function
    return [item for item in gen]

class XrangeTest(unittest.TestCase):
    """This is the test of xrange_funcfunction"""
    def test1(self):
        """This function compares create_list function result with expected"""
        self.assertEqual(create_list(1, 10, 2), [1, 3, 5, 7, 9])
        self.assertEqual(create_list(1, 6), [1, 2, 3, 4, 5])
        self.assertEqual(create_list(5), [0, 1, 2, 3, 4])
        self.assertEqual(create_list(-5), [])
        self.assertEqual(create_list(-5, 1), [-5, -4, -3, -2, -1, 0])
        self.assertEqual(create_list(-5, 1, 2), [-5, -3, -1])
        self.assertEqual(create_list(5, -1, -2), [5, 3, 1])
        self.assertEqual(create_list(-10, -3, 2), [-10, -8, -6, -4])
        self.assertEqual(create_list(-10, -5), [-10, -9, -8, -7, -6])
        self.assertEqual(create_list(-5, -10, -1), [-5, -6, -7, -8, -9])
        self.assertEqual(create_list(-10, -5, -1), [])

if __name__ == '__main__':
    unittest.main()
