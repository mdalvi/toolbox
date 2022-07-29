import importlib


def get_class_from_string(module_name: str, class_name: str):
    """
    https://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class
    :param module_name:
    :param class_name:
    :return:
    """
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def get_duplicates_in_list(lst):
    """
    https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a-list-and-create-another-list-with-them
    """
    seen1 = set()
    seen2 = set()

    seen1_add = seen1.add
    seen2_add = seen2.add

    for item in lst:
        if item in seen1:
            seen2_add(item)
        else:
            seen1_add(item)

    return list(seen2)

