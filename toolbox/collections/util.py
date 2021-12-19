def get_duplicate_items(iterable: list):
    """
    https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
    :param iterable:
    :return:
    """
    seen_once = set()
    seen_twice = set()
    seen_add = seen_once.add
    seen_twice_add = seen_twice.add
    for item in iterable:
        if item in seen_once:
            seen_twice_add(item)
        else:
            seen_add(item)
    return list(seen_twice)
