import concurrent.futures

from loguru import logger

from src.bot import bot
from src.bursbot import BursBot
from src.db import mongodb
from src.scraper import Scraper

if __name__ == '__main__':
    bursbot = BursBot(telebot=bot, db=mongodb)
    scraper = Scraper()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(bursbot.run)
        executor.submit(scraper.run)
