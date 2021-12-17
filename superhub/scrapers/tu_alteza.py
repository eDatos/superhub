from pathlib import Path

import pandas as pd

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap(self):
        tables = pd.read_html(self.config['url'], header=0)
        df = pd.concat(tables)
        self.save_dataframe(df)
