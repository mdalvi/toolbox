def get_embedding_size(n_cat: int) -> int:
    """
    Determines the embedding vector size for number of categories
    https://github.com/fastai/fastai/blob/96c5927648ecf83f0bc9ab601f672d3c0ffe0059/fastai/tabular/data.py#L13
    :param n_cat: number of categories
    :return: int
    """
    return int(min(600, round(1.6 * n_cat ** 0.56)))