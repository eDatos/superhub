import shutil
from pathlib import Path

import pandas as pd
from logzero import logger

import settings


def save_dataframe(establishments, df_output_path):
    logger.info(f'Saving dataframe to {df_output_path}')
    if isinstance(establishments, pd.DataFrame):
        df = establishments
    else:
        # establishments expected to be list[dict]
        df = pd.DataFrame(establishments)
    df.to_csv(df_output_path, index=False)


def compress_data(
    df_folder: Path = settings.DF_OUTPUT_FOLDER,
    output_filepath: Path = settings.ZIPDATA_FILEPATH,
):
    logger.info(f'Compressing output data -> {output_filepath}')
    return shutil.make_archive(output_filepath.stem, 'zip', df_folder)
