
def flatten(l):
    ...


assert flatten([]) == []
assert flatten([1, 2, 3]) == [1, 2, 3]
assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
assert flatten([1, 2, [3, 4, [5, 6], 7], 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
assert flatten([[[[[[[[[[[[[[[[[[[[[1, [1]]]]]]]]]]]]]]]]]]]]]]) == [1, 1]