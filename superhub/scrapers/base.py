from pathlib import Path

import pandas as pd
from logzero import logger

import settings
from superhub import network, utils


class BaseScraper:
    def __init__(
        self,
        slug: str,
        config: dict,
        use_webdriver=False,
        df_output_folder: Path = settings.DF_OUTPUT_FOLDER,
    ):
        logger.info(f'Building {slug.upper()} scraper')
        self.slug = slug
        self.config = config[slug]
        self.df_output_path = df_output_folder / (slug + '.csv')
        if use_webdriver:
            self.webdriver = utils.setup_webdriver()
        else:
            self.webdriver = None

    def __str__(self):
        return f'{self.config["slug"]} -> {self.config["url"]}'

    def __del__(self):
        if self.webdriver is not None:
            self.webdriver.quit()

    def scrap(self):
        raise NotImplementedError()

    def make_request(self, url, method='get', include_user_agent=True):
        return network.make_request(
            url, method=method, include_user_agent=include_user_agent
        )

    def save_dataframe(self, establishments):
        logger.info(f'Saving dataframe to {self.df_output_path}')
        if isinstance(establishments, pd.DataFrame):
            df = establishments
        else:
            # establishments expected to be list[dict]
            df = pd.DataFrame(establishments)
        df.to_csv(self.df_output_path, index=False)
