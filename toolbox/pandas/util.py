import logging
import sys
from glob import glob
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def save_dataframes(path_name, **kwargs: {str: pd.DataFrame}) -> None:
    for kwargs_name, kwargs_obj in kwargs.items():
        pd.to_pickle(kwargs_obj, f'{path_name}/{kwargs_name}.pkl')


def load_dataframes(path_name):
    global logger

    result = list()
    logger.debug(f"Loading dataframes from path {path_name}")
    for folder_name in glob(f"{path_name}/*"):
        dataset_data = dict()
        for file_name in glob(f"{folder_name}/*.pkl"):
            # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
            logger.debug(f'Invoking pd.DataFrame.read_pickle({file_name})')
            dataset_data[Path(file_name).stem] = pd.read_pickle(Path(file_name))
        result.append(dataset_data)
    return result


def replace_inf(df: pd.DataFrame) -> pd.DataFrame:
    global logger
    logger.debug(f'Invoking pd.DataFrame.replace(-np.inf and +np.inf, np.nan)')
    return df.replace(-np.inf, np.nan).replace(np.inf, np.nan)


def concat_files_in_folder(path: str, extension: str = 'csv') -> pd.DataFrame:
    global logger

    # https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
    path_name = f"{path}/*.{extension}"
    logger.debug(f'Globing files from path {path_name}')

    all_files = glob(path_name)
    data_frames = []

    logger.debug(f'Total {len(all_files)} files found')
    for filename in all_files:
        logger.debug(f'Reading file {filename}')
        df = pd.read_csv(filename, index_col=None, header=0)
        data_frames.append(df)

    logger.debug(f'Invoking pd.DataFrame.concat(data_frames, , axis=0, ignore_index=True)')
    return pd.concat(data_frames, axis=0, ignore_index=True)
