# TODO: add numba support
def get_school_round(a_in, n_in):
    """
    https://stackoverflow.com/questions/33019698/how-to-properly-round-up-half-float-numbers-in-python
    :param a_in:
    :param n_in:
    :return: float
    """
    if (a_in * 10 ** (n_in + 1)) % 10 == 5:
        return round(a_in + 1 / 10 ** (n_in + 1), n_in)
    else:
        return round(a_in, n_in)


def round_nearest(num: float, to: float) -> float:
    """
    Credited to Paul H.
    https://stackoverflow.com/questions/28425705/python-round-a-float-to-nearest-0-05-or-to-multiple-of-another-float
    :param num:
    :param to:
    :return: float
    """
    return round(num / to) * to
