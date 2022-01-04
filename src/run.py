import emoji
from loguru import logger

from src.bot import bot
from src.constants import bot_messages, keyboards, keys, states
from src.data import DATA_DIR
from src.db import mongodb
from src.users import Users
from src.utils.io import read_json


class BursBot():
    """
    Burs Telegram Bot.
    """
    def __init__(self, telebot, db):
        self.bot = telebot

        # register handlers
        self.handlers()

        # database
        self.db = db

        # Load stock symbols
        self.stock_symbols = read_json(DATA_DIR / 'stock_symbols.json')

    def handlers(self):
        @self.bot.middleware_handler(update_types=['message'])
        def init_handlers(bot_instance, message):
            self.user = Users(chat_id=message.chat.id, bursbot= self, mongodb=self.db, message= message)
            message.text = emoji.demojize(message.text)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            start_text = f'سلام <strong>{message.chat.first_name}</strong>، خوش اومدی :man_raising_hand:'
            start_text += '\n\n  نماد بورسی مورد نظرتو تایپ کن:'
            self.send_message(
                message.chat.id,
                start_text,
                reply_markup=keyboards.main
                )

        @self.bot.message_handler(func=lambda message: message.text in self.stock_symbols)
        def stock(message):
            self.user.update_current_symbol(message.text)
            # TODO: show basic information of the symbol to user
            self.send_message(
                message.chat.id,
                f'<strong>{message.text}</strong>',
                reply_markup=keyboards.stock
            )

        @self.bot.message_handler(regexp=keys.add_stock)
        def add_stock(message):
            current_symbol = self.user.current_symbol
            portfolio = self.user.portfolio
            portfolio[current_symbol] = self.stock_symbols[current_symbol]
            self.user.update_portfolio(portfolio)

            self.send_message(
                message.chat.id,
                f"{current_symbol} {bot_messages.stock_added} {bot_messages.new_symbol}",
                reply_markup=keyboards.main
                )

        @self.bot.message_handler(regexp=keys.portfolio)
        def portfolio(message):
            portfolio_text = bot_messages.portfolio
            portfolio_text += ':radio_button:'
            portfolio_text += '\n :radio_button: '.join(self.user.portfolio.keys())
            self.send_message(
                message.chat.id,
                portfolio_text,
                reply_markup=keyboards.exit
                )

        @self.bot.message_handler(regexp=keys.exit)
        def exit(message):
            self.send_message(
                message.chat.id,
                (bot_messages.exit + bot_messages.new_symbol),
                reply_markup=keyboards.main
                )

        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            self.send_message(message.chat.id, (bot_messages.not_stock + bot_messages.new_symbol))

    def run(self):
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message for telegram bot.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

if __name__ == '__main__':
    logger.info('Bot Started!')
    tlgrmbot = BursBot(telebot=bot, db=mongodb)
    tlgrmbot.run()
