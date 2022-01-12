import requests

from src.constants import urls
from src.data import DATA_DIR
from src.utils.io import read_json


class Stock:
    def __init__(self):
        # Load stock symbols
        self.all_symbols = read_json(DATA_DIR / 'stock_symbols.json')

    def get_symbol_info(self, url):
        # Scrapping
        response = requests.get(url, timeout=5)
        return response.text.split(";")[0].split(",")

    def last_price(self, symbol):
        url = self.get_symbol_info_url(symbol)
        return self.get_symbol_info(url)[2]

    def get_symbol_info_url(self, symbol):
        index = self.all_symbols[symbol]['index']
        return urls.TSE_SYMBOL_INFO.format(index=index)
