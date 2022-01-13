import re
import time
from pathlib import Path

import pandas as pd
from logzero import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import BaseScraper


class Scraper(BaseScraper):
    def __init__(self, config: dict):
        slug = Path(__file__).stem
        super().__init__(slug, config, use_webdriver=True)

    def parse_place(self, place: FirefoxWebElement):
        name = place.find_element_by_tag_name('h3').text
        if not name:
            return
        details = place.find_element_by_tag_name('p')
        address, place, region = re.split(r'\n+', details.text)[:3]
        return address.strip(), place.strip(), region.strip(' ()')

    def scrap(self):
        self.webdriver.get(self.config['url'])
        WebDriverWait(self.webdriver, 10).until(
            EC.presence_of_element_located((By.ID, self.config['id_to_wait_for']))
        )
        location_input = self.webdriver.find_element_by_id(self.config['location_input_id'])
        location_input.send_keys(self.config['search_text'])
        time.sleep(1)
        pac_container = self.webdriver.find_element_by_class_name(
            self.config['pac_container_class']
        )
        pac_items = pac_container.find_elements_by_class_name(self.config['pac_item_class'])
        first_pac_item = pac_items[0]
        first_pac_item.click()

        logger.debug('Parsing places')
        data = []
        for place in self.webdriver.find_elements_by_class_name(self.config['place_class']):
            if fields := self.parse_place(place):
                data.append(fields)

        df = pd.DataFrame(data, columns=self.config['columns'])
        self.save_dataframe(df)
