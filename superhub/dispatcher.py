from importlib import import_module

import yaml

import settings
from superhub import notification, storage


class Dispatcher:
    def __init__(self, config_path: str = settings.CONFIG_FILEPATH):
        with open(config_path) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def scrap(self, slug: str):
        scraper_module = import_module(f'superhub.scrapers.{slug}')
        scraper = scraper_module.Scraper(self.config)
        scraper.scrap()

    def scrap_all(self, filter=[]):
        for slug in self.config:
            enabled = self.config[slug].get('enabled', True)
            if enabled and (not filter or (slug in filter)):
                self.scrap(slug)

    def compress(self):
        storage.compress_data()

    def notify(self):
        notification.notify()
