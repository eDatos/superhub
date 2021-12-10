from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, url: str):
        super().__init__('Carrefour', url)

    def scrap(self):
        print(self)
