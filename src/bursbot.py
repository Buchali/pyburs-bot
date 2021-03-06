import emoji
from loguru import logger

from src.scraper import Scraper
from src.bot import bot
from src.db import mongodb
from src.handlers import CallbackQueryHandler, MessageHandler


class BursBot():
    """
    Burs Telegram Bot.
    """
    def __init__(self, telebot, db):
        # telebot
        self.bot = telebot

        # database
        self.db = db

        # scraper
        self.scraper = Scraper()

        # register handlers
        self.handlers = [
            MessageHandler(bursbot=self, db=self.db),
            CallbackQueryHandler(bursbot=self, db=self.db),
        ]
        self.register()

    def register(self):
        for handler in self.handlers:
            handler.register()

    def run(self):
        """
        Run the bot.
        """
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message for telegram bot.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def answer_callback_query(self, call_id, text, emojize=True):
        """
        Answer callback.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.answer_callback_query(call_id, text=text)

    def delete_message(self, chat_id, message_id: str):
        """
        Delete bot message.
        """
        self.bot.delete_message(chat_id=chat_id, message_id=message_id)

if __name__ == '__main__':
    logger.info('Bot Started!')
    bursbot = BursBot(telebot=bot, db=mongodb)
    bursbot.run()
