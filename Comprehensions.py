"""This functions are written to practice list comprehensions"""
def squares(nums):
    """This function returns squares of input list items"""
    return [n * n for n in nums]

def odd(nums):
    """This function returns each input list item, situated on odd position"""
    return [n for n in nums[1::2]]

def odd2(nums):
    """This function returns square of each even input list item, situated on odd position"""
    return [n * n for n in nums[1::2] if n%2 == 0]

def test(got, expected):
    """Simple function, used in main() to print what each
	function returns vs. what it's supposed to return."""
    if got == expected:
        prefix = ' OK'
    else:
        prefix = ' X'
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))

def main():
    """This is the test of squares() function"""
    test(squares([1, -2, 3]), [1, 4, 9])
    test(odd([1, 4, 3, 5, 5, 2]), [4, 5, 2])
    test(odd2([1, 4, 3, 5, 5, 2]), [16, 4])

if __name__ == '__main__':
    main()
