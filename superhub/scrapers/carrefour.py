from pathlib import Path

import pandas as pd

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap(self):
        target_field = self.config['target_field']['name']
        target_postal_codes = [str(tpc) for tpc in self.config['target_field']['values']]
        response = self.make_request(self.config['url'])
        # TODO: response.status_code
        df = pd.read_xml(response.text)
        df = df[df[target_field].str[:2].isin(target_postal_codes)]
        df.to_csv(self.df_output_path, index=False)
