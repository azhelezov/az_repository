"""This functions are written to practice list comprehensions"""
def squares(nums):
    """This function prints squares of input list items"""
    print 'Input list: ' + str(nums)
    squared_list = [n * n for n in nums]
    return 'Result list: ' + str(squared_list)
print squares([1, 4, 3])

def odd(nums):
    """This function prints each input list item, situated on odd position"""
    print 'Input list: ' + str(nums)
    odd_list = [n for n in nums[1::2]]
    return 'Result list: ' + str(odd_list)
print odd([1, 4, 3, 5, 5, 2])

def odd2(nums):
    """This function prints squares of each even input list item, situated on odd position"""
    print 'Input list: ' + str(nums)
    odd_list = [n * n for n in nums[1::2] if n%2 == 0]
    return 'Result list: ' + str(odd_list)
print odd2([1, 4, 3, 5, 5, 2])
