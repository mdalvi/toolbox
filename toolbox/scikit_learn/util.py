import logging
import sys
from glob import glob
from pathlib import Path

import numpy as np
from joblib import dump, load

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def save_extras(path_name: str, **kwargs: {str: object}) -> None:
    for kwargs_name, kwargs_obj in kwargs.items():
        dump(kwargs_obj, f'{path_name}/{kwargs_name}.joblib')


def load_extras(path_name: str) -> list:
    global logger

    result = list()
    logger.debug(f"Loading extras from path {path_name}")
    for folder_name in glob(f"{path_name}/*"):
        extras_data = dict()
        for file_name in glob(f"{folder_name}/*.joblib"):
            # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
            logger.debug(f'Invoking joblib.load({file_name})')
            extras_data[Path(file_name).stem] = load(Path(file_name))
        result.append(extras_data)
    return result


def expected_calibration_error(y, proba, bins='fd'):
    """
    https://towardsdatascience.com/pythons-predict-proba-doesn-t-actually-predict-probabilities-and-how-to-fix-it-f582c21d63fc
    """
    bin_count, bin_edges = np.histogram(proba, bins=bins)
    n_bins = len(bin_count)
    bin_edges[0] -= 1e-8  # because left edge is not included
    bin_id = np.digitize(proba, bin_edges, right=True) - 1
    bin_ysum = np.bincount(bin_id, weights=y, minlength=n_bins)
    bin_probasum = np.bincount(bin_id, weights=proba, minlength=n_bins)
    bin_ymean = np.divide(bin_ysum, bin_count, out=np.zeros(n_bins), where=bin_count > 0)
    bin_probamean = np.divide(bin_probasum, bin_count, out=np.zeros(n_bins), where=bin_count > 0)
    ece = np.abs((bin_probamean - bin_ymean) * bin_count).sum() / len(proba)
    return ece
