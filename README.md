# superhub

Set of scrapers written in Python to retrieve address information (and hopefully some more) about supermarket chains in Canary Islands.

## Setup

Create a Python virtualenv and install requirements:

```console
$ python3.10 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

User settings are defined in [settings.py](settings.py). For those settings without any default value, you must create an `.env` file in the working directory and give them a value. Optionally, you can overwrite any others.

Scraping rules (for trades) are defined in [config.yml](config.yml). You can change it on demand.

### Other requirements

There are few external requirements for the project to work properly:

- [geckodriver](https://github.com/mozilla/geckodriver/releases)
- [Firefox Browser](https://www.mozilla.org/firefox/download/)

## Usage

```console
$ python main.py --help
Usage: main.py [OPTIONS]

Options:
  -v, --verbose      Loglevel increased to debug.
  -t, --trades TEXT  Trades to be scraped. Empty value implies all trades.
  -x, --compress     Compress output data files.
  -n, --notify       Notify output data files. --compress is implicit.
  --help             Show this message and exit.
```

A common usage would be just `python main.py -vn` which will scrap all "enabled" trades, download, compress and notify them via email.

## Output data

For each trade (supermarket chain) defined in [config.yml](config.yml) a **csv file** is generated within a `data` folder.

Each file has different columns since it depends on the available data at the scraped website. Each row represents an establishment for the respective trade.

## Changelog

Check [features and bugfixes](CHANGELOG.md) for each release.
