from pathlib import Path

import pandas as pd

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap(self):
        url = self.config['url'].format(
            lat=self.config['lat'], lon=self.config['lon'], radius=self.config['radius']
        )
        response = self.make_request(url)
        df = pd.read_xml(response.text)
        self.save_dataframe(df)
