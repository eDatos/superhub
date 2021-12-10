from importlib import import_module

import yaml

import settings


class Dispatcher:
    def __init__(self, config_path: str = settings.CONFIG_FILEPATH):
        with open(config_path) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def scrap(self, chain: str, url: str):
        chain_module = import_module(f'superhub.scrapers.{chain}')
        scraper = chain_module.Scraper(url)
        scraper.scrap()

    def scrap_all(self, filter=[]):
        for chain, fields in self.config.items():
            if (not filter) or (chain in filter):
                self.scrap(chain, fields['url'])
