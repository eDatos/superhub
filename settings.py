from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_FILEPATH = config('CONFIG_FILEPATH', default=PROJECT_DIR / 'config.yml', cast=Path)
DEBUG_CHAINS = config('DEBUG_CHAINS', default=[], cast=config.list)
SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))

DF_OUTPUT_FOLDER = config('DF_OUTPUT_FOLDER', default=PROJECT_DIR / 'data', cast=Path)
