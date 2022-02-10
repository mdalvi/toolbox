import os
from glob import glob
from pathlib import Path

import numpy as np
import pandas as pd


def dump_dataframes(path_name, **kwargs: {str: pd.DataFrame}) -> None:
    for kwargs_name, kwargs_obj in kwargs.items():
        pd.to_pickle(kwargs_obj, f'{path_name}/{kwargs_name}.pkl')


def load_dataframes(path_name: str) -> list:
    result = list()
    for folder_name in glob(f"{path_name}/*"):
        if os.path.isdir(folder_name):
            dataset_data = dict()
            for file_name in glob(f"{folder_name}/*.pkl"):
                # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
                dataset_data[Path(file_name).stem] = pd.read_pickle(Path(file_name))
            result.append(dataset_data)
    return result


def replace_inf(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(-np.inf, np.nan).replace(np.inf, np.nan)


def concat_files_in_folder(path: str, extension: str = 'csv') -> pd.DataFrame:
    # https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
    path_name = f"{path}/*.{extension}"

    all_files = glob(path_name)
    data_frames = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        data_frames.append(df)

    return pd.concat(data_frames, axis=0, ignore_index=True)
