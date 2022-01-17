import emoji
from loguru import logger
from telebot import types


def create_keyboard(
    *keys,
    row_width=2, resize_keyboard=True,
    is_inline=False, inline_row_width=4, callback_data=None
    ):
    """
    create a keyboard from keys
    """
    keys = list(keys)
    if callback_data and (len(keys) != len(callback_data)):
        logger.warning('Callback data length is not equal to keys length. Some keys will be missing.')

    # Empty keyboard
    if not keys:
        return

    if is_inline:
        # Inline keyboard
        if callback_data is None:
            callback_data = keys

        markup = types.InlineKeyboardMarkup(
            row_width=inline_row_width
            )

        buttons = []
        for ind, key in enumerate(keys):
            key = emoji.emojize(key)
            buttons.append(types.InlineKeyboardButton(key, callback_data=callback_data[ind]))

        markup.add(*buttons)
        return markup

    # Regular keyboard
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width,
        resize_keyboard=resize_keyboard
        )
    markup.add(*buttons)
    return markup
