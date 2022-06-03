import emoji
from constants.constant_keyboards import inline_keyboards, keyboards, keys
from constants.constant_other import portfo_attr, states
from src.constants import constant_message
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
                constant_message.START.format(first_name=message.chat.first_name),
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
                constant_message.ISIN_PORTFOLIO.format(message.text),
                reply_markup=keyboards.main
            )

        @self.bursbot.bot.message_handler(func=lambda message: message.text in self.bursbot.scraper.symbols_info)
        def symbol(message):
            """
            Handles all new symbols typed by the user.
            """
            self.bursbot.user.update_current_symbol(message.text)
            self.bursbot.send_message(
                message.chat.id,
                constant_message.SYMBOL_INFO.format(
                    symbol=message.text,
                    last_price=self.bursbot.scraper.get_symbol_data(message.text)['pl']
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
                    constant_message.STOP_LOSS_ADDED.format(
                        symbol=current_symbol
                    ),
                    reply_markup=keyboards.main
                )
            elif (self.bursbot.user.state == states.TAKE_PROFIT):
                portfolio[current_symbol][portfo_attr.TAKE_PROFIT] = int(message.text)
                self.bursbot.send_message(
                    message.chat.id,
                    constant_message.TAKE_PROFIT_ADDED.format(
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
            portfolio[current_symbol] = self.bursbot.scraper.symbols_info[current_symbol]
            self.bursbot.user.update_portfolio(portfolio)

            self.bursbot.send_message(
                message.chat.id,
                constant_message.ADD_SYMBOL.format(symbol=current_symbol),
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
                constant_message.EMPTY_PORTFOLIO,
                reply_markup=keyboards.exit
                )
                return

            # Porfolio is not empty
            self.bursbot.send_message( message.chat.id,
            constant_message.PORTFOLIO,
            reply_markup=keyboards.exit
            )

            # Send each symbol in a seperate message with inline keys
            for mysymbol in self.bursbot.user.portfolio.keys():
                stop_loss = self.bursbot.user.portfolio[mysymbol].get(portfo_attr.STOP_LOSS) or 'NA'
                take_profit = self.bursbot.user.portfolio[mysymbol].get(portfo_attr.TAKE_PROFIT) or 'NA'
                self.bursbot.send_message(
                    message.chat.id,
                    constant_message.PORTFOLIO_SYMBOL.format(
                        symbol=mysymbol,
                        last_price=self.bursbot.scraper.get_symbol_data(mysymbol)['pl'],
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
                constant_message.EXIT,
                reply_markup=keyboards.main
                )
            self.bursbot.user.update_state(states.MAIN)

        @self.bursbot.bot.message_handler(func=lambda m: True)
        def unidentifed(message):
            """
            User typed an unidentifed symbol, message, command ...
            """
            self.bursbot.send_message(message.chat.id, constant_message.NOT_SYMBOL.format(symbol=message.text))
