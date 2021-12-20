import json
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
            search_radius=self.config['search_radius'],
        )
        response = self.make_request(url)
        start = response.text.find('(')
        return json.loads(response.text[start + 1 : -1])['d']['results']

    def scrap(self):
        establishments = []
        for island in self.config['islands']:
            establishments += self.scrap_island(island)

        df = pd.DataFrame(establishments)
        df.drop_duplicates(subset=['Locality', 'AddressLine'], inplace=True)
        # some cleaning
        df['OpeningTimes'] = df['OpeningTimes'].str.replace(r'(<br/?>)+', ' ', regex=True)
        df['OpeningTimes'] = df['OpeningTimes'].str.replace(r'(</?b>)+', '', regex=True)
        df = df[
            [
                'PostalCode',
                'Locality',
                'AddressLine',
                'OpeningTimes',
                'Longitude',
                'Latitude',
            ]
        ]
        self.save_dataframe(df)
