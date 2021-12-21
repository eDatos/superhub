import shutil
from importlib import import_module

import yaml
from logzero import logger

import settings


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
            if (not filter) or (slug in filter):
                self.scrap(slug)

    def compress(self):
        output_filepath = settings.ZIPDATA_FILEPATH
        logger.info(f'Compressing output data -> {output_filepath}')
        return shutil.make_archive(output_filepath.stem, 'zip', settings.DF_OUTPUT_FOLDER)
