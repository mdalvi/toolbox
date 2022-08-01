def get_embedding_size(n_cat: int) -> int:
    """
    Determines the embedding vector size for number of categories
    https://github.com/fastai/fastai/blob/0a01eba7de66bd5430295d09517a0ad530d9ff66/fastai/tabular/model.py#L15
    :param n_cat: number of categories
    :return: int
    """
    return int(min(600, round(1.6 * n_cat ** 0.56)))
