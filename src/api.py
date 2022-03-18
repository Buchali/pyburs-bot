import requests

from src.constants import urls
from src.data import DATA_DIR
from src.utils.io import read_json


class BursAPI:
    """
    A class for scrapping burs symbol's info.
    """
    def __init__(self):
        # Load all symbols
        self.all_symbols = read_json(DATA_DIR / 'all_symbols.json')

    def get_symbol_info(self, url: str) -> list:
        """
        Scrapes all the symbol information using the url and return them in a list.
        """
        try:
            response = requests.get(url, timeout=5)
            return response.text.split(";")[0].split(",")
        except:
            return None

    def last_price(self, symbol: str) -> int:
        """
        Scrape the last price using the symbol name.
        """
        url = self.get_symbol_info_url(symbol)
        try:
            lprice = self.get_symbol_info(url)[2]
            return int(lprice)
        except:
            return None

    def get_symbol_info_url(self, symbol: str):
        """
        Gives back the url using the symbol name.
        """
        index = self.all_symbols[symbol]['index']
        return urls.TSE_SYMBOL_INFO.format(index=index)
