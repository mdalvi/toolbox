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
