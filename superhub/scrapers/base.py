import time
from pathlib import Path

import pandas as pd
import requests
import user_agent
from logzero import logger

import settings
from superhub import utils


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
        logger.debug(f'Requesting {url}')
        if req_delay := self.config.get('req_delay'):
            logger.debug(f'Delay of {req_delay} seconds')
            time.sleep(req_delay)
        if include_user_agent:
            ua = user_agent.generate_user_agent()
            headers = {'User-Agent': ua}
        else:
            headers = {}
        f = getattr(requests, method)
        try:
            response = f(url, headers=headers, timeout=settings.REQUESTS_TIMEOUT)
        except requests.exceptions.ReadTimeout as err:
            logger.error(err)
        else:
            logger.debug(f'Response status code: {response.status_code}')
            return response

    def save_dataframe(self, establishments: list[dict]):
        logger.info(f'Saving dataframe to {self.df_output_path}')
        df = pd.DataFrame(establishments)
        df.to_csv(self.df_output_path, index=False)
