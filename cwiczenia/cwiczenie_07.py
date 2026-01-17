
def flatten(collection):
    flatten_collection = []
    for item in collection:
        if isinstance(item, list):
            flatten_collection.extend(flatten(item))
        else:
            flatten_collection.append(item)
    return flatten_collection


type([]) == list
isinstance([], list)
assert flatten([]) == []
assert flatten([1, 2, 3]) == [1, 2, 3]
assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
assert flatten([1, 2, [3, 4, [5, 6], 7], 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
assert flatten([[[[[[[[[[[[[[[[[[[[[1, [1]]]]]]]]]]]]]]]]]]]]]]) == [1, 1]