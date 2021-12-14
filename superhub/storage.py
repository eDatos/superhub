import pandas as pd
from logzero import logger


def save_dataframe(establishments, df_output_path):
    logger.info(f'Saving dataframe to {df_output_path}')
    if isinstance(establishments, pd.DataFrame):
        df = establishments
    else:
        # establishments expected to be list[dict]
        df = pd.DataFrame(establishments)
    df.to_csv(df_output_path, index=False)
