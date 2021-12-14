from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from logzero import logger

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def parse_location(self, location: str):
        name = location.h3.string.strip()
        address = location.select('div.building > dl > dd:nth-child(2)')[0].string
        address = address.strip().replace(' ', '')
        phone = location.select('div.building > dl > dd:nth-child(4) > a')[0].string
        phone = phone.strip().replace(' ', '')
        return dict(name=name, address=address, phone=phone)

    def scrap_establishment(self, url: str):
        if (response := self.make_request(url)) is None:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.parse_location(soup.find(id='location'))

    def extract_urls_from_province(self, url: str):
        if (response := self.make_request(url)) is None:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        dropdown = soup.find(id='shopping_centers_dropdown')
        for link in dropdown.find_all('a', 'dropdown-item'):
            # link is relative
            yield urljoin(response.url, link['href'])

    def scrap(self):
        establishments = []
        for province_url in self.config['url']:
            for url in self.extract_urls_from_province(province_url):
                if url is None:
                    logger.error('Non reachable URL')
                else:
                    if (fields := self.scrap_establishment(url)) is None:
                        logger.error('Location fields are not available')
                    else:
                        establishments.append(fields)
        self.save_dataframe(establishments)
