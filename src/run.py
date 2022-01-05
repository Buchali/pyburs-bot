import emoji
from loguru import logger

import constants
from src.bot import bot
from src.constants import keyboards, keys, states
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
            self.user.update_state(states.MAIN)
            self.send_message(
                message.chat.id,
                constants.START_MESSAGE.format(first_name=message.chat.first_name),
                reply_markup=keyboards.main
                )
        @self.bot.message_handler(func=lambda message: message.text in self.user.portfolio)
        def portfolio_symbol(message):
            self.user.update_current_symbol(message.text)
            # user wants to delete a symbol
            if self.user.state == states.DELETE:
                portfolio = self.user.portfolio
                deleted_symbol = portfolio.pop(message.text, None)
                if deleted_symbol is None:
                    self.send_message(
                    message.chat.id,
                    constants.NOT_IN_PORTFOLIO_MESSAGE.format(symbol=message.text),
                    reply_markup=keyboards.portfolio
                    )
                    self.user.update_state(states.PORTFOLIO)
                else:
                    self.user.update_portfolio(portfolio)
                    self.send_message(
                    message.chat.id,
                    constants.DELETED_MESSAGE.format(symbol=message.text),
                    reply_markup=keyboards.main
                    )
                    self.user.update_state(states.MAIN)

        @self.bot.message_handler(func=lambda message: message.text in self.stock_symbols)
        def symbol(message):
            self.user.update_current_symbol(message.text)

            # TODO: show basic information of the symbol to user
            self.send_message(
                message.chat.id,
                f"<strong>{self.stock_symbols[message.text]['name']}</strong>",
                reply_markup=keyboards.symbol
            )

        @self.bot.message_handler(regexp=keys.add_symbol)
        def add_symbol(message):
            current_symbol = self.user.current_symbol
            portfolio = self.user.portfolio
            portfolio[current_symbol] = self.stock_symbols[current_symbol]
            self.user.update_portfolio(portfolio)

            self.send_message(
                message.chat.id,
                constants.ADD_SYMBOL_MESSAGE.format(symbol=current_symbol),
                reply_markup=keyboards.main
                )
            self.user.update_state(states.MAIN)

        @self.bot.message_handler(regexp=keys.portfolio)
        def portfolio(message):
            if not self.user.portfolio.keys():
                self.send_message(
                message.chat.id,
                constants.EMPTY_PORTFOLIO_MESSAGE,
                reply_markup=keyboards.exit
                )
                return

            portfolio_text = '\n'.join(self.user.portfolio.keys())
            self.send_message(
                message.chat.id,
                constants.PORTFOLIO_MESSAGE.format(portfolio=portfolio_text),
                reply_markup=keyboards.portfolio
                )
            self.user.update_state(states.PORTFOLIO)

        @self.bot.message_handler(regexp=keys.delete_symbol)
        def delete_symbol(message):
            self.send_message(
                message.chat.id,
                constants.DELETE_SYMBOL_MESSAGE,
                reply_markup=keyboards.exit
                )
            self.user.update_state(states.DELETE)

        @self.bot.message_handler(regexp=keys.exit)
        def exit(message):
            self.send_message(
                message.chat.id,
                constants.EXIT_MESSAGE,
                reply_markup=keyboards.main
                )
            self.user.update_state(states.MAIN)

        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            self.send_message(message.chat.id, constants.NOT_SYMBOL_MESSAGE.format(symbol=message.text))

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
