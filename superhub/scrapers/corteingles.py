from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def parse_location(self, location: str):
        name = location.h3.string
        return name

    def scrap_establishment(self, url: str):
        response = self.make_request(url)
        # TODO: response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')
        self.parse_location(soup.find(id='location'))

    def extract_urls_from_province(self, url: str):
        response = self.make_request(url)
        # TODO: response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')
        dropdown = soup.find(id='shopping_centers_dropdown')
        for link in dropdown.find_all('a', 'dropdown-item'):
            # link is relative
            yield urljoin(response.url, link['href'])

    def scrap(self):
        for province_url in self.config['url']:
            for url in self.extract_urls_from_province(province_url):
                self.scrap_establishment(url)
