import logging
import sys

import pandas as pd
from sklearn.feature_selection import VarianceThreshold

from ..pandas.util import replace_inf

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def get_y(y: pd.DataFrame, id_column: str, label_column: str) -> pd.Series:
    """
    To convert traditional target series y to tsfresh compatible series y
    """
    y = y[[id_column, label_column]].drop_duplicates([id_column, label_column], keep='first')
    y = y[[id_column, label_column]].drop_duplicates([id_column], keep='last')
    y.set_index(id_column, inplace=True)
    y.index.name = None
    return y


def filter_no_variance_columns(df: pd.DataFrame, threshold: float = 0.0) -> pd.DataFrame:
    global logger

    df = replace_inf(df)

    # drop column having only np.nan values
    # https://stackoverflow.com/questions/45147100/pandas-drop-columns-with-all-nans
    df.dropna(axis=1, how='all', inplace=True)

    logger.debug(f'Invoking VarianceThreshold(threshold={threshold}).fit()')
    variance_threshold = VarianceThreshold(threshold=threshold)
    variance_threshold.fit(df)

    logger.debug(f'Filtering dataframe')
    return df[df.columns[variance_threshold.variances_ > threshold]]
