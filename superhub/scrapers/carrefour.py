from pathlib import Path

import pandas as pd
import requests

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap(self):
        target_field = self.config['target_field']['name']
        target_postal_codes = self.config['target_field']['values']

        response = requests.get(self.config['url'])
        df = pd.read_xml(response.text)
        df = df[df[target_field].str[:2].isin(target_postal_codes)]
        df.to_csv(self.df_output_path, index=False)
