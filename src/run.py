import emoji
from loguru import logger

import constants
from src.bot import bot
from src.constants import keyboards, keys, states
from src.db import mongodb
from src.stock import Stock
from src.users import Users


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

        # Load stock
        self.stock = Stock()

    def handlers(self):
        @self.bot.middleware_handler(update_types=['message'])
        def init_handlers(bot_instance, message):
            """
            Initialize Handelers.
            """
            self.user = Users(chat_id=message.chat.id, bursbot= self, mongodb=self.db, message= message)
            message.text = emoji.demojize(message.text)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            Handles '/start' command.
            """
            self.user.update_state(states.MAIN)
            self.send_message(
                message.chat.id,
                constants.START_MESSAGE.format(first_name=message.chat.first_name),
                reply_markup=keyboards.main
                )
        @self.bot.message_handler(func=lambda message: message.text in self.user.portfolio)
        def portfolio_symbol(message):
            """
            Handles portfolio symbols.
            """
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

        @self.bot.message_handler(func=lambda message: message.text in self.stock.all_symbols)
        def symbol(message):
            """
            Handles all symbols except the portfolio ones.
            """
            self.user.update_current_symbol(message.text)
            self.send_message(
                message.chat.id,
                constants.SYMBOL_INFO_MESSAGE.format(
                    symbol=message.text,
                    last_price=self.stock.last_price(message.text)
                ),
                reply_markup=keyboards.symbol
            )

        @self.bot.message_handler(regexp=keys.add_symbol)
        def add_symbol(message):
            """
            Add symbol to portfolio
            """
            current_symbol = self.user.current_symbol
            portfolio = self.user.portfolio
            portfolio[current_symbol] = self.stock.all_symbols[current_symbol]
            self.user.update_portfolio(portfolio)

            self.send_message(
                message.chat.id,
                constants.ADD_SYMBOL_MESSAGE.format(symbol=current_symbol),
                reply_markup=keyboards.main
                )
            self.user.update_state(states.MAIN)

        @self.bot.message_handler(regexp=keys.portfolio)
        def portfolio(message):
            """
            Display portfolio.
            """
            # Notify if portfolio is empty.
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
            """
            Delete a symbol from portfolio
            """
            self.send_message(
                message.chat.id,
                constants.DELETE_SYMBOL_MESSAGE,
                reply_markup=keyboards.exit
                )
            self.user.update_state(states.DELETE)

        @self.bot.message_handler(regexp=keys.exit)
        def exit(message):
            """
            Exit and back to Main state.
            """
            self.send_message(
                message.chat.id,
                constants.EXIT_MESSAGE,
                reply_markup=keyboards.main
                )
            self.user.update_state(states.MAIN)

        @self.bot.message_handler(func=lambda m: True)
        def unidentifed(message):
            """
            User typed an unidentifed symbol, message, command ...
            """
            self.send_message(message.chat.id, constants.NOT_SYMBOL_MESSAGE.format(symbol=message.text))

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

if __name__ == '__main__':
    logger.info('Bot Started!')
    tlgrmbot = BursBot(telebot=bot, db=mongodb)
    tlgrmbot.run()
