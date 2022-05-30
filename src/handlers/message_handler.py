import emoji
from src import constants
from src.constants import (inline_keyboards, keyboards, keys, portfo_attr,
                           states)
from src.users import Users


class MessageHandler:
    def __init__(self, bursbot, db):
        self.bursbot = bursbot
        self.db = db

    def register(self):
        @self.bursbot.bot.middleware_handler(update_types=['message'])
        def init_handlers(bot_instance, message):
            """
            Initialize Handelers.
            """
            self.bursbot.user = Users(chat_id=message.chat.id, bursbot= self.bursbot, mongodb=self.db)
            message.text = emoji.demojize(message.text)

        @self.bursbot.bot.message_handler(commands=['start'])
        def start(message):
            """
            Handles '/start' command.
            """
            self.bursbot.send_message(
                message.chat.id,
                constants.START_MESSAGE.format(first_name=message.chat.first_name),
                reply_markup=keyboards.main
                )
            self.bursbot.user.update_state(states.MAIN)

        @self.bursbot.bot.message_handler(func=lambda message: message.text in self.bursbot.user.portfolio)
        def portfolio_symbol(message):
            """
            Send message to user when typing a portfolio symbol.
            """
            self.bursbot.user.update_current_symbol(message.text)
            self.bursbot.send_message(
                message.chat.id,
                constants.ISIN_PORTFOLIO_MESSAGE.format(message.text),
                reply_markup=keyboards.main
            )

        @self.bursbot.bot.message_handler(func=lambda message: message.text in self.bursbot.scraper.all_symbols)
        def symbol(message):
            """
            Handles all new symbols typed by the user.
            """
            self.bursbot.user.update_current_symbol(message.text)
            self.bursbot.send_message(
                message.chat.id,
                constants.SYMBOL_INFO_MESSAGE.format(
                    symbol=message.text,
                    last_price=self.bursbot.scraper.last_price(message.text)
                ),
                reply_markup=keyboards.symbol
            )

        @self.bursbot.bot.message_handler(func=lambda message: message.text.isnumeric())
        def set_limit(message):
            """
            setting limit for symbols.
            """
            current_symbol = self.bursbot.user.current_symbol
            if not current_symbol:
                return

            portfolio = self.bursbot.user.portfolio
            if (self.bursbot.user.state == states.STOP_LOSS):
                portfolio[current_symbol][portfo_attr.STOP_LOSS] = int(message.text)
                self.bursbot.send_message(
                    message.chat.id,
                    constants.STOP_LOSS_ADDED_MESSAGE.format(
                        symbol=current_symbol
                    ),
                    reply_markup=keyboards.main
                )
            elif (self.bursbot.user.state == states.TAKE_PROFIT):
                portfolio[current_symbol][portfo_attr.TAKE_PROFIT] = int(message.text)
                self.bursbot.send_message(
                    message.chat.id,
                    constants.TAKE_PROFIT_ADDED_MESSAGE.format(
                        symbol=current_symbol
                    ),
                    reply_markup=keyboards.main
                )

            self.bursbot.user.update_portfolio(portfolio)

        @self.bursbot.bot.message_handler(regexp=keys.add_symbol)
        def add_symbol(message):
            """
            Add symbol to portfolio
            """
            current_symbol = self.bursbot.user.current_symbol
            portfolio = self.bursbot.user.portfolio
            portfolio[current_symbol] = self.bursbot.scraper.all_symbols[current_symbol]
            self.bursbot.user.update_portfolio(portfolio)

            self.bursbot.send_message(
                message.chat.id,
                constants.ADD_SYMBOL_MESSAGE.format(symbol=current_symbol),
                reply_markup=keyboards.main
                )
            self.bursbot.user.update_state(states.MAIN)

        @self.bursbot.bot.message_handler(regexp=keys.portfolio)
        def portfolio(message):
            """
            Display portfolio symbols.
            """
            # Notify if portfolio is empty.
            if not self.bursbot.user.portfolio.keys():
                self.bursbot.send_message(
                message.chat.id,
                constants.EMPTY_PORTFOLIO_MESSAGE,
                reply_markup=keyboards.exit
                )
                return

            # Porfolio is not empty
            self.bursbot.send_message( message.chat.id,
            constants.PORTFOLIO_MESSAGE,
            reply_markup=keyboards.exit
            )

            # Send each symbol in a seperate message with inline keys
            for mysymbol in self.bursbot.user.portfolio.keys():
                stop_loss = self.bursbot.user.portfolio[mysymbol].get(portfo_attr.STOP_LOSS) or 'NA'
                take_profit = self.bursbot.user.portfolio[mysymbol].get(portfo_attr.TAKE_PROFIT) or 'NA'
                self.bursbot.send_message(
                    message.chat.id,
                    constants.PORTFOLIO_SYMBOL_MESSAGE.format(
                        symbol=mysymbol,
                        last_price=self.bursbot.scraper.last_price(mysymbol),
                        stop_loss=stop_loss, take_profit=take_profit
                    ),
                    reply_markup=inline_keyboards.portfolio
                    )
            self.bursbot.user.update_state(states.PORTFOLIO)

        @self.bursbot.bot.message_handler(regexp=keys.exit)
        def exit(message):
            """
            Exit and back to Main state.
            """
            self.bursbot.send_message(
                message.chat.id,
                constants.EXIT_MESSAGE,
                reply_markup=keyboards.main
                )
            self.bursbot.user.update_state(states.MAIN)

        @self.bursbot.bot.message_handler(func=lambda m: True)
        def unidentifed(message):
            """
            User typed an unidentifed symbol, message, command ...
            """
            self.bursbot.send_message(message.chat.id, constants.NOT_SYMBOL_MESSAGE.format(symbol=message.text))
