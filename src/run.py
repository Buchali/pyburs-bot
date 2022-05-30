import emoji
from loguru import logger

from src.bot import bot
from src.db import mongodb
from src.handlers import CallbackQueryHandler, MessageHandler
from scraper import Scraper

class BursBot():
    """
    Burs Telegram Bot.
    """
    def __init__(self, telebot, db):
        # telebot
        self.bot = telebot

        # scraper
        self.scraper = Scraper()

        # database
        self.db = db

        # register handlers
        self.handlers = [
            MessageHandler(bursbot=self, db=self.db),
            CallbackQueryHandler(bursbot=self, db=self.db),
        ]
        self.register()

    def register(self):
        for handler in self.handlers:
            handler.register()
    # def handlers(self):
        # @self.bot.middleware_handler(update_types=['message'])
        # def init_handlers(bot_instance, message):
        #     """
        #     Initialize Handelers.
        #     """
        #     self.user = Users(chat_id=message.chat.id, bursbot= self, mongodb=self.db)
        #     message.text = emoji.demojize(message.text)

        # @self.bot.message_handler(commands=['start'])
        # def start(message):
        #     """
        #     Handles '/start' command.
        #     """
        #     self.send_message(
        #         message.chat.id,
        #         constants.START_MESSAGE.format(first_name=message.chat.first_name),
        #         reply_markup=keyboards.main
        #         )
        #     self.user.update_state(states.MAIN)

        # @self.bot.message_handler(func=lambda message: message.text in self.user.portfolio)
        # def portfolio_symbol(message):
        #     """
        #     Send message to user when typing a portfolio symbol.
        #     """
        #     self.user.update_current_symbol(message.text)
        #     self.send_message(
        #         message.chat.id,
        #         constants.ISIN_PORTFOLIO_MESSAGE.format(message.text),
        #         reply_markup=keyboards.main
        #     )

        # @self.bot.message_handler(func=lambda message: message.text in self.scraper.all_symbols)
        # def symbol(message):
        #     """
        #     Handles all new symbols typed by the user.
        #     """
        #     self.user.update_current_symbol(message.text)
        #     self.send_message(
        #         message.chat.id,
        #         constants.SYMBOL_INFO_MESSAGE.format(
        #             symbol=message.text,
        #             last_price=self.scraper.last_price(message.text)
        #         ),
        #         reply_markup=keyboards.symbol
        #     )

        # @self.bot.message_handler(func=lambda message: message.text.isnumeric())
        # def set_limit(message):
        #     """
        #     setting limit for symbols.
        #     """
        #     current_symbol = self.user.current_symbol
        #     if not current_symbol:
        #         return

        #     portfolio = self.user.portfolio
        #     if (self.user.state == states.STOP_LOSS):
        #         portfolio[current_symbol][portfo_attr.STOP_LOSS] = int(message.text)
        #         self.send_message(
        #             message.chat.id,
        #             constants.STOP_LOSS_ADDED_MESSAGE.format(
        #                 symbol=current_symbol
        #             ),
        #             reply_markup=keyboards.main
        #         )
        #     elif (self.user.state == states.TAKE_PROFIT):
        #         portfolio[current_symbol][portfo_attr.TAKE_PROFIT] = int(message.text)
        #         self.send_message(
        #             message.chat.id,
        #             constants.TAKE_PROFIT_ADDED_MESSAGE.format(
        #                 symbol=current_symbol
        #             ),
        #             reply_markup=keyboards.main
        #         )

        #     self.user.update_portfolio(portfolio)

        # @self.bot.message_handler(regexp=keys.add_symbol)
        # def add_symbol(message):
        #     """
        #     Add symbol to portfolio
        #     """
        #     current_symbol = self.user.current_symbol
        #     portfolio = self.user.portfolio
        #     portfolio[current_symbol] = self.scraper.all_symbols[current_symbol]
        #     self.user.update_portfolio(portfolio)

        #     self.send_message(
        #         message.chat.id,
        #         constants.ADD_SYMBOL_MESSAGE.format(symbol=current_symbol),
        #         reply_markup=keyboards.main
        #         )
        #     self.user.update_state(states.MAIN)

        # @self.bot.message_handler(regexp=keys.portfolio)
        # def portfolio(message):
        #     """
        #     Display portfolio symbols.
        #     """
        #     # Notify if portfolio is empty.
        #     if not self.user.portfolio.keys():
        #         self.send_message(
        #         message.chat.id,
        #         constants.EMPTY_PORTFOLIO_MESSAGE,
        #         reply_markup=keyboards.exit
        #         )
        #         return

        #     # Porfolio is not empty
        #     self.send_message( message.chat.id,
        #     constants.PORTFOLIO_MESSAGE,
        #     reply_markup=keyboards.exit
        #     )

        #     # Send each symbol in a seperate message with inline keys
        #     for mysymbol in self.user.portfolio.keys():
        #         stop_loss = self.user.portfolio[mysymbol].get(portfo_attr.STOP_LOSS) or 'NA'
        #         take_profit = self.user.portfolio[mysymbol].get(portfo_attr.TAKE_PROFIT) or 'NA'
        #         self.send_message(
        #             message.chat.id,
        #             constants.PORTFOLIO_SYMBOL_MESSAGE.format(
        #                 symbol=mysymbol,
        #                 last_price=self.scraper.last_price(mysymbol),
        #                 stop_loss=stop_loss, take_profit=take_profit
        #             ),
        #             reply_markup=inline_keyboards.portfolio
        #             )
        #     self.user.update_state(states.PORTFOLIO)

        # @self.bot.callback_query_handler(func=lambda call: call.data in inline_keys.stop_loss)
        # def stop_loss_callback(call):
        #     """
        #     Stop loss call back.
        #     """
        #     current_symbol = call.message.text.splitlines()[0]
        #     self.answer_callback_query(call.id, text=call.data)
        #     self.send_message(
        #         call.message.chat.id,
        #         constants.ASK_STOP_LOSS_MESSAGE.format(
        #             symbol=current_symbol
        #         ),
        #         reply_markup=keyboards.exit
        #     )
        #     self.user.update_state(states.STOP_LOSS)
        #     self.user.update_current_symbol(current_symbol)

        # @self.bot.callback_query_handler(func=lambda call: call.data in inline_keys.take_profit)
        # def take_profit_callback(call):
        #     """
        #     Take profit call back.
        #     """
        #     current_symbol = call.message.text.splitlines()[0]
        #     self.answer_callback_query(call.id, text=call.data)
        #     self.send_message(
        #         call.message.chat.id,
        #         constants.ASK_TAKE_PROFIT_MESSAGE.format(
        #             symbol=current_symbol
        #         ),
        #         reply_markup=keyboards.exit
        #     )
        #     self.user.update_state(states.TAKE_PROFIT)
        #     self.user.update_current_symbol(current_symbol)

        # @self.bot.callback_query_handler(func=lambda call: call.data in inline_keys.delete_symbol)
        # def delete_symbol(call):
        #     """
        #     Delete a symbol from portfolio.
        #     """
        #     current_symbol = call.message.text.splitlines()[0]
        #     self.answer_callback_query(
        #         call.id,
        #         text=constants.DELETED_MESSAGE.format(symbol=current_symbol)
        #         )
        #     portfolio = self.user.portfolio
        #     portfolio.pop(current_symbol)
        #     self.user.update_portfolio(portfolio)

        #     # Delete the symbol from portfolio instantly
        #     self.delete_message(
        #         chat_id=call.message.chat.id,
        #         message_id=call.message.message_id
        #         )

        # @self.bot.message_handler(regexp=keys.exit)
        # def exit(message):
        #     """
        #     Exit and back to Main state.
        #     """
        #     self.send_message(
        #         message.chat.id,
        #         constants.EXIT_MESSAGE,
        #         reply_markup=keyboards.main
        #         )
        #     self.user.update_state(states.MAIN)

        # @self.bot.message_handler(func=lambda m: True)
        # def unidentifed(message):
        #     """
        #     User typed an unidentifed symbol, message, command ...
        #     """
        #     self.send_message(message.chat.id, constants.NOT_SYMBOL_MESSAGE.format(symbol=message.text))

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
    tlgrmbot = BursBot(telebot=bot, db=mongodb)
    tlgrmbot.run()
