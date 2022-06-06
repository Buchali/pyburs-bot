import concurrent.futures
import time
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
        self.symbols = list(symbols_info.keys())

    def get_symbol_url(self, symbol: str) -> str:
        """
        Get symbol url based on its symbol.
        """
        index = (self.symbols_info[symbol]['index'])
        return urls.TSE_SYMBOL_INFO.format(index=index)

    def scrape_symbol_data(self, symbol: str) -> dict:
        """
        Scrapes the instant data using the url.
        """
        keys = ['time', 'state', 'pl', 'pc',
                'pf', 'py', 'pmin', 'pmax',
                'tno', 'tvol','tval']
        symbol_url = self.get_symbol_url(symbol)
        try:
            response = requests.get(symbol_url, timeout=2)
            values = response.text.split(";")[0].split(",")
        except:
            values = []

        return dict(zip_longest(keys, values))

    def get_symbol_data(self, symbol: str) -> dict:
        """
        Returns the symbol's data.
        """
        symbols_data_path = DATA_DIR / 'symbols_data.json'
        if symbols_data_path.exists():
            symbols_data = read_json(symbols_data_path)
            return symbols_data[symbol]

        return self.scrape_symbol_data(symbol)

    def scrape_all_data(self) -> dict:
        """
        Scrapes all symbols' data.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.scrape_symbol_data, self.symbols)

        return dict(zip(self.symbols, list(results)))

    def download_all_data_json(self):
        """
        Writes all symbols' data to json file.
        """
        symbols_data = self.scrape_all_data()
        logger.info(f'Writing {len(symbols_data)} symbols data to json file.')
        write_json(symbols_data, DATA_DIR / 'symbols_data.json', ensure_ascii=False)

    def run(self, interval: int = 300):
        """
        Scrapes all symbols' data regularly every [interval] sec.
        """
        while True:
            logger.info('Scraping Starts...')
            self.download_all_data_json()
            logger.info("All Data Scraped succussfully.")
            time.sleep(interval)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.download_all_data()
    logger.info('DONE')
