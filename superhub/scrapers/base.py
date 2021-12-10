class BaseScraper:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def __str__(self):
        return f'{self.name} -> {self.url}'

    def scrap(self):
        raise NotImplementedError()
