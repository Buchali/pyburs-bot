import emoji
from src import constants
from src.constants import inline_keys, keyboards, states
from src.users import Users


class CallbackQueryHandler:
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

        @self.bursbot.bot.callback_query_handler(func=lambda call: call.data in inline_keys.stop_loss)
        def stop_loss_callback(call):
            """
            Stop loss call back.
            """
            current_symbol = call.message.text.splitlines()[0]
            self.bursbot.answer_callback_query(call.id, text=call.data)
            self.bursbot.send_message(
                call.message.chat.id,
                constants.ASK_STOP_LOSS_MESSAGE.format(
                    symbol=current_symbol
                ),
                reply_markup=keyboards.exit
            )
            self.bursbot.user.update_state(states.STOP_LOSS)
            self.bursbot.user.update_current_symbol(current_symbol)

        @self.bursbot.bot.callback_query_handler(func=lambda call: call.data in inline_keys.take_profit)
        def take_profit_callback(call):
            """
            Take profit call back.
            """
            current_symbol = call.message.text.splitlines()[0]
            self.bursbot.answer_callback_query(call.id, text=call.data)
            self.bursbot.send_message(
                call.message.chat.id,
                constants.ASK_TAKE_PROFIT_MESSAGE.format(
                    symbol=current_symbol
                ),
                reply_markup=keyboards.exit
            )
            self.bursbot.user.update_state(states.TAKE_PROFIT)
            self.bursbot.user.update_current_symbol(current_symbol)

        @self.bursbot.bot.callback_query_handler(func=lambda call: call.data in inline_keys.delete_symbol)
        def delete_symbol(call):
            """
            Delete a symbol from portfolio.
            """
            current_symbol = call.message.text.splitlines()[0]
            self.bursbot.answer_callback_query(
                call.id,
                text=constants.DELETED_MESSAGE.format(symbol=current_symbol)
                )
            portfolio = self.bursbot.user.portfolio
            portfolio.pop(current_symbol)
            self.bursbot.user.update_portfolio(portfolio)

            # Delete the symbol from portfolio instantly
            self.bursbot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
                )
