import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import settings


class BaseScraper:
    def __init__(
        self,
        slug: str,
        config: dict,
        use_webdriver=False,
        df_output_folder: Path = settings.DF_OUTPUT_FOLDER,
    ):
        self.slug = slug
        self.config = config[slug]
        self.df_output_path = df_output_folder / (slug + '.csv')
        if use_webdriver:
            self.webdriver = self.setup_webdriver()
        else:
            self.webdriver = None

    def __str__(self):
        return f'{self.config["slug"]} -> {self.config["url"]}'

    def __del__(self):
        if self.webdriver is not None:
            self.webdriver.quit()

    def scrap(self):
        raise NotImplementedError()

    def setup_webdriver(self, headless: bool = settings.SELENIUM_HEADLESS):
        options = Options()
        options.headless = headless
        profile = webdriver.FirefoxProfile()
        return webdriver.Firefox(
            options=options, firefox_profile=profile, log_path=os.devnull
        )
