import emoji
from loguru import logger

from src.bot import bot
from src.constants import bot_messages, keyboards, keys, states
from src.db import mongodb
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

    def handlers(self):
        @self.bot.middleware_handler(update_types=['message'])
        def init_handlers(bot_instance, message):
            self.user = Users(chat_id=message.chat.id, bursbot= self, mongodb=self.db, message= message)
            message.text = emoji.demojize(message.text)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.send_message(
                 message.chat.id,
                f'{bot_messages.start} <strong>{message.chat.first_name}</strong>!',
                reply_markup=keyboards.main
                )

            self.user.update_state(states.main)

        @self.bot.message_handler(regexp = keys.add_stock)
        def add_stock(message):
            self.send_message(
                 message.chat.id,
                bot_messages.add_stock,
                reply_markup=keyboards.exit
                )
            stock_name = message.text
            self.user.update_state(states.add_stock)

        @self.bot.message_handler(regexp = keys.exit)
        def exit(message):
            self.send_message(
                 message.chat.id,
                bot_messages.exit,
                reply_markup=keyboards.main
                )
            self.user.update_state(states.main)

        @self.bot.message_handler(func=lambda m: True)
        def echo(message):
            self.send_message(
                message.chat.id, message.text,
                reply_markup=keyboards.main
            )

    def run(self):
        logger.info('Bot is running...')
        self.bot.infinity_polling()

    def send_message(self, chat_id, text, reply_markup=None, demojize=True):
        """
        send message for telegram bot.
        """
        if demojize:
            text = emoji.demojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

if __name__ == '__main__':
    logger.info('Bot Started!')
    tlgrmbot = BursBot(telebot=bot, db=mongodb)
    tlgrmbot.run()
