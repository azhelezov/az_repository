"""This functions are written to practice list comprehensions"""
import unittest


def squares(inp_list):
    """This function returns squares of input list items"""
    return [item * item for item in inp_list]

def odd_pos(inp_list):
    """This function returns each input list item, situated on odd position"""
    return [item for item in inp_list[1::2]]

def square_evenitems_oddpos(inp_list):
    """This function returns square of each even input list item, situated on odd position"""
    return [item * item for item in inp_list[1::2] if item%2 == 0]

class XrangeTest(unittest.TestCase):
    """This is the test of xrange_funcfunction"""
    def test1(self):
        """This function compares create_list function result with expected"""
        self.assertEqual(squares([1, -2, 3]),
                         [1, 4, 9])
        self.assertEqual(odd_pos([1, 4, 3, 5, 5, 2]),
                         [4, 5, 2])
        self.assertEqual(square_evenitems_oddpos([1, 4, 3, 5, 5, 2]),
                         [16, 4])

if __name__ == '__main__':
    unittest.main()
