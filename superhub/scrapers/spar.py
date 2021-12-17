from pathlib import Path

import pandas as pd
from logzero import logger

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap_island(self, island: str) -> list[dict]:
        logger.debug(f'Scraping {island.upper()}')
        url = self.config['url'].format(
            lat=self.config['islands'][island]['lat'],
            lon=self.config['islands'][island]['lon'],
            max_results=self.config['max_results'],
            search_radius=self.config['search_radius'],
        )
        response = self.make_request(url)
        return response.json()

    def scrap(self):
        establishments = []
        for island in self.config['islands']:
            establishments += self.scrap_island(island)

        df = pd.DataFrame(establishments)
        df.drop_duplicates(subset=['address', 'city'], inplace=True)
        self.save_dataframe(df)
