"""This is the realization of zip() function"""
import unittest


def zip_func(*args):
    """This function returns a list of tuples, where the i-th tuple contains
    the i-th element from each of the argument sequences or iterables"""
    mylist = [] # Creating a new list
    min_length = min(len(item) for item in args) # Searching for the argument
                                                 # with a minimum length
    for args_item in xrange(min_length): # Adding tuples to the mylist
        mylist.append(tuple(item[args_item] for item in args),)
    return mylist

class XrangeTest(unittest.TestCase):
    """This is the test of zip_func function"""
    def test1(self):
        """This function compares zip_func function result with expected"""
        self.assertEqual(zip_func(['bear', 'rabbit', 'tiger'], [3, 7, 1], ['a']),
                         [('bear', 3, 'a')])
        self.assertEqual(zip_func('apple', (16, 17, 35)),
                         [('a', 16), ('p', 17), ('p', 35)])

if __name__ == '__main__':
    unittest.main()
