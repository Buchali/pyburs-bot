import concurrent.futures

from loguru import logger

from src.bot import bot
from src.bursbot import BursBot
from src.db import mongodb
from src.scraper import Scraper

if __name__ == '__main__':
    bursbot = BursBot(telebot=bot, db=mongodb)
    scraper = Scraper()
    logger.info("Multi-processing is starting ...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        r = executor.submit(bursbot.run)
        r = executor.submit(scraper.run)
