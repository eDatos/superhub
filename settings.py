from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_FILEPATH = config('CONFIG_FILEPATH', default=PROJECT_DIR / 'config.yml', cast=Path)
SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))

DF_OUTPUT_FOLDER = config('DF_OUTPUT_FOLDER', default=PROJECT_DIR / 'data', cast=Path)

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)

# seconds
REQUESTS_TIMEOUT = config('REQUESTS_TIMEOUT', default=5, cast=int)
