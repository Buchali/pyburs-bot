import concurrent.futures
from itertools import zip_longest

import requests
from loguru import logger

from constants.constant_url import urls
from src.data import DATA_DIR
from src.utils.io import read_json, write_json


class Scraper:
    """
    A class for scrapping Tehran Stock Exchange symbol's info.
    """
    def __init__(self):
        # Load all symbols
        symbols_info = read_json(DATA_DIR / 'symbols_info.json')
        self.symbols_info = symbols_info
        symbols_urls = []
        symbols = []
        for symbol in symbols_info:
            symbols_urls.append(self.get_symbol_url(symbol))
            symbols.append(symbol)

        self.symbols = symbols
        self.symbol_urls = symbols_urls

    def get_symbol_url(self, symbol: str) -> str:
        """
        Get symbol url based on its symbol.
        """
        index = (self.symbols_info[symbol]['index'])
        return urls.TSE_SYMBOL_INFO.format(index=index)

    def scrape_symbol_url(self, symbol_url: str) -> dict:
        """
        Scrapes the instant data using the url.
        """
        keys = ['time', 'state', 'pl', 'pc',
                'pf', 'py', 'pmin', 'pmax',
                'tno', 'tvol','tval']

        try:
            response = requests.get(symbol_url, timeout=5)
            values = response.text.split(";")[0].split(",")
        except:
            values = []

        return dict(zip_longest(keys, values))

    def get_symbol_data(self, symbol: str) -> dict:
        """
        Returns the symbol's data.
        """
        symbol_url = self.get_symbol_url(symbol)
        return self.scrape_symbol_url(symbol_url)

    def scrape_all_data(self) -> dict:
        """
        Scrapes all symbols' instant data.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(self.scrape_symbol_url, self.symbol_urls)

        return dict(zip(self.symbols, list(results)))

    def write_all_data_json(self):
        """
        Writes all symbols' instant data to json file.
        """
        symbols_data = self.scrape_all_data()
        logger.info(f'Writing {len(symbols_data)} symbols data to json file.')
        write_json(symbols_data, DATA_DIR / 'symbols_data.json', ensure_ascii=False)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.write_all_data_json()
