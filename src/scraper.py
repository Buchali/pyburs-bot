import concurrent.futures
from itertools import zip_longest

import requests
from loguru import logger

from constants.constant_url import urls
from src.data import DATA_DIR
from src.utils.io import read_json


class Scraper:
    """
    A class for scrapping Tehran Stock Exchange symbol's info.
    """
    def __init__(self):
        # Load all symbols
        stocks_info = read_json(DATA_DIR / 'stocks_info.json')
        symbols_urls = []
        symbols = []
        for symbol in stocks_info:
            index = (stocks_info[symbol]['index'])
            symbols_urls.append(urls.TSE_SYMBOL_INFO.format(index=index))
            symbols.append(symbol)

        self.stocks_info = stocks_info
        self.symbols = symbols
        self.stock_urls = symbols_urls

    def scrape_stock_url(self, stock_url: str) -> dict:
        """
        Scrapes the instant data using the url.
        """
        keys = ['time', 'state',
          'pl', 'pc',
          'pf', 'py',
          'pmin', 'pmax',
          'tno', 'tvol',
          'tval']

        try:
            response = requests.get(stock_url, timeout=5)
            values = response.text.split(";")[0].split(",")
        except:
            values = []

        return dict(zip_longest(keys, values))

    def scrape_instant_data(self) -> dict:
        """
        Scrapes all symbols' instant data.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(self.scrape_stock_url, self.stock_urls)

        return dict(zip(self.symbols, list(results)))

if __name__ == '__main__':
    scraper = Scraper()
    all_data = scraper.scrape_instant_data()
    example = all_data['پالایش']
    logger.info(example)
