import json
import re
from pathlib import Path

import pandas as pd

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def scrap(self):
        response = self.make_request(self.config['url'])
        places = re.findall(r'"places":(\[\{.*\}\]),"styles"', response.text)
        contents = []
        for place in places:
            data = json.loads(place)
            contents += data

        df = pd.json_normalize(contents)
        df = df.rename(
            columns={
                'content': 'phone',
                'location.lat': 'latitude',
                'location.lng': 'longitude',
                'location.postal_code': 'postal',
            }
        )
        df['phone'] = df['phone'].str.extract(r'(\d{3}[\d ]+)')
        df = df[['title', 'address', 'postal', 'phone', 'latitude', 'longitude']]
        self.save_dataframe(df)
