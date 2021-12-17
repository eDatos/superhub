from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import Tag
from logzero import logger

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config)

    def get_num_pages(self):
        if (response := self.make_request(self.config['url'])) is None:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        num_pages_table = soup.find('div', class_='table-container--pagination__numeration')
        num_pages_span = list(num_pages_table.h2.find_all('span'))[1]
        return int(num_pages_span.string)

    def scrap_establishment(self, establishment: Tag) -> dict:
        name = establishment.h3.string.strip()
        other_fields = [p.get_text().strip() for p in establishment.find_all('p')]
        address = other_fields[0]
        match len(other_fields):
            case 2:
                timetable = None
                phone = other_fields[1]
            case 3:
                timetable = other_fields[1]
                phone = other_fields[2]

        return dict(name=name, address=address, timetable=timetable, phone=phone)

    def scrap_page(self, url) -> list[dict]:
        if (response := self.make_request(url)) is None:
            return None
        page_establishments = []
        soup = BeautifulSoup(response.text, 'html.parser')
        establishments = soup.find_all('div', class_='tienda__item')
        for establishment in establishments:
            fields = self.scrap_establishment(establishment)
            page_establishments.append(fields)
        return page_establishments

    def scrap(self):
        establishments = []
        num_pages = self.get_num_pages()
        search_url = self.config['url'] + '?p={num_page}'
        for num_page in range(1, num_pages + 1):
            logger.debug(f'Scraping page {num_page}')
            url = search_url.format(num_page=num_page)
            if (page_establishments := self.scrap_page(url)) is None:
                logger.debug('Non reachable URL')
            else:
                establishments.extend(page_establishments)

        self.save_dataframe(establishments)
